import base64
from io import BytesIO
from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.models import load_model, model_from_json
from tensorflow.python.keras.models import Model as LegacyModel
from tensorflow.python.keras.models import model_from_json as legacy_model_from_json

from backend.config import Config


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
    if _model is not None:
        return _model

    model_path = Path(Config.MODEL_PATH)
    if model_path.exists():
        try:
            _model = load_model(model_path, compile=False)
            return _model
        except Exception:
            pass

    with open(Config.MODEL_JSON_PATH, "r", encoding="utf-8") as file:
        model_json = file.read()

    # Keras 3 may fail to deserialize older Functional JSON configs.
    try:
        _model = model_from_json(model_json)
    except Exception:
        _model = legacy_model_from_json(model_json)

    _model.load_weights(Config.MODEL_WEIGHTS_PATH)
    return _model


def predict_image(base64_image):
    pil_image = _decode_image(base64_image)
    model_input = _to_model_input(pil_image)
    model = get_model()
    # Use direct forward-pass inference to avoid legacy predict() internals
    # that can break on mixed TF/Keras versions.
    prediction_tensor = model(model_input, training=False)
    prediction = np.array(prediction_tensor)[0]

    if prediction.ndim == 0:
        prediction = np.array([1 - float(prediction), float(prediction)])

    if len(prediction) == 2:
        labels = ["No Tumor", "Tumor"]
    else:
        labels = CLASS_NAMES[: len(prediction)]

    predicted_index = int(np.argmax(prediction))
    confidence = float(prediction[predicted_index] * 100.0)
    predicted_class = labels[predicted_index]

    return {
        "predictedClass": predicted_class,
        "confidence": round(confidence, 2),
        "scores": {labels[i]: round(float(prediction[i]) * 100.0, 2) for i in range(len(labels))},
        "pilImage": pil_image,
    }


def _encode_np_image(image_np):
    rgb_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    _, buffer = cv2.imencode(".png", rgb_image)
    return base64.b64encode(buffer.tobytes()).decode("utf-8")


def generate_gradcam(base64_image):
    model = get_model()
    pil_image = _decode_image(base64_image)
    model_input = _to_model_input(pil_image)

    conv_layer = None
    for layer in reversed(model.layers):
        if len(layer.output_shape) == 4:
            conv_layer = layer.name
            break

    if conv_layer is None:
        original = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        encoded = _encode_np_image(original)
        return {
            "originalImage": encoded,
            "heatmapImage": encoded,
            "overlayImage": encoded,
        }

    # Build Grad-CAM model with the same model family to avoid
    # KerasTensor type mismatches between legacy/new keras.
    is_legacy_model = "tensorflow.python.keras" in str(type(model))
    model_builder = LegacyModel if is_legacy_model else tf.keras.models.Model
    model_input_tensor = model.inputs[0] if isinstance(model.inputs, (list, tuple)) else model.inputs
    model_output_tensor = model.output[0] if isinstance(model.output, (list, tuple)) else model.output
    grad_model = model_builder(
        inputs=model_input_tensor,
        outputs=[model.get_layer(conv_layer).output, model_output_tensor],
    )

    try:
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(model_input)
            index = tf.argmax(predictions[0])
            class_channel = predictions[:, index]
    except Exception:
        # Graceful fallback if Grad-CAM graph build fails in mixed TF/Keras env.
        original = cv2.cvtColor(np.array(pil_image.resize((224, 224))), cv2.COLOR_RGB2BGR)
        encoded = _encode_np_image(original)
        return {
            "originalImage": encoded,
            "heatmapImage": encoded,
            "overlayImage": encoded,
        }

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    heatmap = heatmap.numpy()

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

    return {
        "originalImage": _encode_np_image(original),
        "heatmapImage": _encode_np_image(heatmap_color),
        "overlayImage": _encode_np_image(overlay),
    }
