from setuptools import setup

install_requires = ["web.py", "cloudpickle"]

setup(
    name='model_envelope',
    version='0.1',
    description='POC of Model Envelope abstration from Stitchfix',
    author='Anand Chitipothu',
    author_email='anandology@gmail.com',
    url='http://anandology.github.com/model-envelope',
    py_modules=['model_envelope'],
    license="MIT",
    platforms=["any"],
    install_requires=install_requires
 )