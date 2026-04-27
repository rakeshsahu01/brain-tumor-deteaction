# Brain Tumor Detection - Heroku Deployment Guide

## Prerequisites
- Heroku CLI installed ([Download](https://devcenter.heroku.com/articles/heroku-cli))
- Git repository initialized
- MongoDB Atlas account (free tier available at https://www.mongodb.com/cloud/atlas)

## Deployment Steps

### 1. Create MongoDB Database
1. Sign up/login to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user and get your connection string
4. Update your `MONGO_URI` with the connection string

### 2. Prepare Your Local Repository
```bash
# Navigate to project root
cd Brain-Tumor-Detection-main

# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit for Heroku deployment"
```

### 3. Create Heroku App
```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Or use existing app
heroku apps:create
```

### 4. Set Environment Variables
```bash
# Set SECRET_KEY
heroku config:set SECRET_KEY="your-secure-random-key"

# Set JWT SECRET
heroku config:set JWT_SECRET_KEY="your-jwt-secret-key"

# Set MongoDB Connection String
heroku config:set MONGO_URI="mongodb+srv://username:password@cluster.mongodb.net/brain_tumor_ai?retryWrites=true&w=majority"

# Set DB Name
heroku config:set DB_NAME="brain_tumor_ai"

# Set Flask Environment
heroku config:set FLASK_ENV="production"
```

### 5. Add Node.js Buildpack
```bash
# Add buildpacks for Python and Node.js
heroku buildpacks:add heroku/nodejs
heroku buildpacks:add heroku/python
```

### 6. Deploy to Heroku
```bash
# Push to Heroku
git push heroku main  # or master, depending on your branch name

# View logs
heroku logs --tail

# Open your app
heroku open
```

## Troubleshooting

### Check App Status
```bash
heroku ps
```

### View Logs
```bash
heroku logs --tail
```

### SSH into Dyno (if needed)
```bash
heroku ps:exec
```

### Reset Database
```bash
heroku config:unset DB_NAME
heroku config:set DB_NAME="brain_tumor_ai"
```

## Important Notes

1. **Model Files**: The `model.h5` and `model.json` files are included in your repository. Ensure they're committed to git.

2. **Static Files**: React frontend is built during deployment and served alongside the Flask backend.

3. **Uploads Directory**: Files uploaded by users will be stored temporarily. For persistence, consider using AWS S3 or Heroku Spaces.

4. **Free Dyno Limitations**: 
   - Free dynos sleep after 30 minutes of inactivity
   - Limited to 512MB RAM
   - For production, upgrade to Hobby or Professional dynos

5. **MongoDB**: Use MongoDB Atlas free tier for development. For production, upgrade to a paid plan.

## Advanced Deployment Options

### Using Heroku Spaces (Private Network)
```bash
heroku spaces:create
```

### Using Heroku Postgres instead of MongoDB
Update `requirements.txt` and `backend/config.py` to use SQLAlchemy with PostgreSQL

### CI/CD with GitHub Actions
Create `.github/workflows/deploy.yml` for automated deployments

## Accessing Your App
- **Web App**: https://your-app-name.herokuapp.com
- **API**: https://your-app-name.herokuapp.com/home
- **API Docs**: https://your-app-name.herokuapp.com/api/docs (if available)

## Support
- Heroku Docs: https://devcenter.heroku.com
- Flask Docs: https://flask.palletsprojects.com
- React Docs: https://react.dev
