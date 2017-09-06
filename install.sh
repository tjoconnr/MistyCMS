#/usr/bin/env sh
echo "Deploying to QA"
appcfg.py --module=qa --version=$BUILD_NUMBER --oauth2_access_token=$GAE_ACCESS --oauth2_refresh_token=$GAE_REFRESH update src/app.yaml
appcfg.py --module=qa --version=$BUILD_NUMBER --oauth2_access_token=$GAE_ACCESS --oauth2_refresh_token=$GAE_REFRESH set_default_version src/app.yaml

echo "Deploying to Production"
appcfg.py --version=$BUILD_NUMBER --oauth2_access_token=$GAE_ACCESS --oauth2_refresh_token=$GAE_REFRESH update src/app.yaml
