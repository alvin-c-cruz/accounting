from accounting import create_app

app = create_app(test_config="test_config.py")
app.config["DEBUG"] = True
app.config["FLASKENV"] = "development"
app.run(port=5000)