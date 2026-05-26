import base64
from io import BytesIO
from pathlib import Path
import logging

import cv2
import numpy as np
from PIL import Image

from backend.config import Config

logger = logging.getLogger(__name__)

# Lazy imports for tensorflow to avoid import errors during backend startup
_tensorflow_loaded = False
tf = None
load_model = None
model_from_json = None
LegacyModel = None
legacy_model_from_json = None


def _load_tensorflow():
    global _tensorflow_loaded, tf, load_model, model_from_json, LegacyModel, legacy_model_from_json
    if _tensorflow_loaded:
        return
    
    try:
        logger.info("Loading TensorFlow...")
        import tensorflow
        from tensorflow.keras.models import load_model as _load_model, model_from_json as _model_from_json
        from tensorflow.python.keras.models import Model as _LegacyModel
        from tensorflow.python.keras.models import model_from_json as _legacy_model_from_json
        
        tf = tensorflow
        load_model = _load_model
        model_from_json = _model_from_json
        LegacyModel = _LegacyModel
        legacy_model_from_json = _legacy_model_from_json
        _tensorflow_loaded = True
        logger.info("TensorFlow loaded successfully")
    except ImportError as e:
        logger.error(f"Failed to load TensorFlow: {e}")
        raise ImportError(f"TensorFlow is required for model loading: {e}")


CLASS_NAMES = ["Glioma", "Meningioma", "Pituitary Tumor", "No Tumor"]

_model = None


def _decode_image(base64_image):
    encoded = base64_image.split(",")[-1]
    image_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    return image


def _to_model_input(pil_image):
    image = np.array(pil_image.resize((224, 224)), dtype=np.float32)
    image = image / 255.0
    return np.expand_dims(image, axis=0)


def get_model():
    global _model
    _load_tensorflow()
    if _model is not None:
        logger.debug("Returning cached model")
        return _model

    logger.info("Loading model...")
    model_path = Path(Config.MODEL_PATH)
    logger.info(f"Checking model path: {model_path}")
    
    if model_path.exists():
        logger.info(f"Model file found at {model_path}, attempting to load...")
        try:
            _model = load_model(model_path, compile=False)
            logger.info("Model loaded successfully from h5 file")
            return _model
        except Exception as e:
            logger.warning(f"Failed to load model from h5: {e}, trying from JSON...")

    logger.info(f"Loading model from JSON: {Config.MODEL_JSON_PATH}")
    try:
        with open(Config.MODEL_JSON_PATH, "r", encoding="utf-8") as file:
            model_json = file.read()
    except FileNotFoundError as e:
        logger.error(f"Model JSON file not found: {Config.MODEL_JSON_PATH}")
        raise FileNotFoundError(f"Model JSON file not found at {Config.MODEL_JSON_PATH}: {e}")

    # Keras 3 may fail to deserialize older Functional JSON configs.
    try:
        logger.info("Attempting to load model from JSON using model_from_json...")
        _model = model_from_json(model_json)
    except Exception as e:
        logger.warning(f"Failed with model_from_json: {e}, trying legacy method...")
        try:
            _model = legacy_model_from_json(model_json)
        except Exception as e2:
            logger.error(f"Failed to load model from JSON with both methods: {e}, {e2}")
            raise

    logger.info(f"Loading model weights from {Config.MODEL_WEIGHTS_PATH}")
    try:
        _model.load_weights(Config.MODEL_WEIGHTS_PATH)
        logger.info("Model weights loaded successfully")
    except FileNotFoundError as e:
        logger.error(f"Model weights file not found: {Config.MODEL_WEIGHTS_PATH}")
        raise FileNotFoundError(f"Model weights not found at {Config.MODEL_WEIGHTS_PATH}: {e}")
    except Exception as e:
        logger.error(f"Failed to load model weights: {e}")
        raise
    
    return _model


def predict_image(base64_image):
    try:
        logger.info("Starting image prediction...")
        pil_image = _decode_image(base64_image)
        logger.debug(f"Image decoded successfully: {pil_image.size}")
        
        model_input = _to_model_input(pil_image)
        logger.debug(f"Model input prepared: shape {model_input.shape}")
        
        model = get_model()
        logger.debug("Model retrieved successfully")
        
        # Use direct forward-pass inference to avoid legacy predict() internals
        # that can break on mixed TF/Keras versions.
        logger.debug("Running model inference...")
        prediction_tensor = model(model_input, training=False)
        prediction = np.array(prediction_tensor)[0]
        logger.debug(f"Raw prediction: {prediction}")

        if prediction.ndim == 0:
            prediction = np.array([1 - float(prediction), float(prediction)])

        if len(prediction) == 2:
            labels = ["No Tumor", "Tumor"]
        else:
            labels = CLASS_NAMES[: len(prediction)]

        predicted_index = int(np.argmax(prediction))
        confidence = float(prediction[predicted_index] * 100.0)
        predicted_class = labels[predicted_index]

        logger.info(f"Prediction complete: {predicted_class} ({confidence:.2f}%)")
        return {
            "predictedClass": predicted_class,
            "confidence": round(confidence, 2),
            "scores": {labels[i]: round(float(prediction[i]) * 100.0, 2) for i in range(len(labels))},
            "pilImage": pil_image,
        }
    except Exception as e:
        logger.error(f"Error during image prediction: {str(e)}", exc_info=True)
        raise


def _encode_np_image(image_np):
    rgb_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    _, buffer = cv2.imencode(".png", rgb_image)
    return base64.b64encode(buffer.tobytes()).decode("utf-8")


def generate_gradcam(base64_image):
    """Generate Grad-CAM visualization with memory optimization."""
    try:
        logger.info("Starting Grad-CAM generation...")
        _load_tensorflow()
        model = get_model()
        logger.debug("Model retrieved for Grad-CAM")
        
        pil_image = _decode_image(base64_image)
        model_input = _to_model_input(pil_image)
        logger.debug("Image prepared for Grad-CAM")

        # Find convolutional layer
        conv_layer = None
        for layer in reversed(model.layers):
            if len(layer.output_shape) == 4:
                conv_layer = layer.name
                logger.debug(f"Found conv layer: {conv_layer}")
                break

        if conv_layer is None:
            logger.warning("No convolutional layer found, using original image")
            original = cv2.cvtColor(np.array(pil_image.resize((224, 224))), cv2.COLOR_RGB2BGR)
            encoded = _encode_np_image(original)
            return {
                "originalImage": encoded,
                "heatmapImage": encoded,
                "overlayImage": encoded,
            }

        # Build Grad-CAM model efficiently
        is_legacy_model = "tensorflow.python.keras" in str(type(model))
        model_builder = LegacyModel if is_legacy_model else tf.keras.models.Model
        model_input_tensor = model.inputs[0] if isinstance(model.inputs, (list, tuple)) else model.inputs
        model_output_tensor = model.output[0] if isinstance(model.output, (list, tuple)) else model.output
        
        grad_model = model_builder(
            inputs=model_input_tensor,
            outputs=[model.get_layer(conv_layer).output, model_output_tensor],
        )
        logger.debug("Grad-CAM model built")

        # Compute gradients
        try:
            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(model_input, training=False)
                index = tf.argmax(predictions[0])
                class_channel = predictions[:, index]
            
            grads = tape.gradient(class_channel, conv_outputs)
        except Exception as e:
            logger.warning(f"Gradient computation failed: {e}, using fallback")
            original = cv2.cvtColor(np.array(pil_image.resize((224, 224))), cv2.COLOR_RGB2BGR)
            encoded = _encode_np_image(original)
            return {
                "originalImage": encoded,
                "heatmapImage": encoded,
                "overlayImage": encoded,
            }

        # Compute heatmap
        logger.debug("Computing heatmap...")
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs_np = conv_outputs[0].numpy()
        pooled_grads_np = pooled_grads.numpy()
        
        # Free TensorFlow memory
        del conv_outputs, grads, class_channel, predictions, grad_model, tape
        tf.keras.backend.clear_session()
        
        # Compute heatmap in numpy to save memory
        heatmap = conv_outputs_np @ pooled_grads_np[..., np.newaxis]
        heatmap = np.squeeze(heatmap)
        heatmap = np.maximum(heatmap, 0) / (np.max(heatmap) + 1e-8)
        
        # Create visualizations
        original = cv2.cvtColor(np.array(pil_image.resize((224, 224))), cv2.COLOR_RGB2BGR)
        heatmap_uint8 = np.uint8(255 * heatmap)
        heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        
        if heatmap_color.shape[:2] != original.shape[:2]:
            heatmap_color = cv2.resize(
                heatmap_color,
                (original.shape[1], original.shape[0]),
                interpolation=cv2.INTER_LINEAR,
            )
        
        overlay = cv2.addWeighted(original, 0.6, heatmap_color, 0.4, 0)

        logger.info("Grad-CAM generation completed successfully")
        return {
            "originalImage": _encode_np_image(original),
            "heatmapImage": _encode_np_image(heatmap_color),
            "overlayImage": _encode_np_image(overlay),
        }
    except Exception as e:
        logger.error(f"Error during Grad-CAM generation: {str(e)}", exc_info=True)
        # Return fallback with original image
        try:
            pil_image = _decode_image(base64_image)
            original = cv2.cvtColor(np.array(pil_image.resize((224, 224))), cv2.COLOR_RGB2BGR)
            encoded = _encode_np_image(original)
            return {
                "originalImage": encoded,
                "heatmapImage": encoded,
                "overlayImage": encoded,
            }
        except Exception as e2:
            logger.error(f"Fallback also failed: {str(e2)}", exc_info=True)
            raise
