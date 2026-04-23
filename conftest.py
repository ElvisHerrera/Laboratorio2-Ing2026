import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
	"""Captura de pantalla automática en caso de fallo"""
	outcome = yield
	report = outcome.get_result()
	extras = getattr(report, "extra", [])
	if report.when == "call" and report.failed:
		# Acceder al driver desde la fixture
		driver = item.funcargs['driver']
		# Convertir la captura a base64 para el reporte HTML
		screenshot = driver.get_screenshot_as_base64()
		html = f'<div><img src="data:image/png;base64,{screenshot}" alt="screenshot" style="width:304px;height:228px;" onclick="window.open(this.src)" align="right"/></div>'
		html_plugin = item.config.pluginmanager.getplugin("html")
		if html_plugin is not None:
			extras.append(html_plugin.extras.html(html))
		report.extra = extras
@pytest.fixture
def driver():
	"""Fixture del navegador"""
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--no-sandbox")
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--disable-gpu")
	driver = webdriver.Chrome(options=options)
	driver.maximize_window()
	yield driver
	driver.quit()