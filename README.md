## ADV- Prog Project Convex Hull MAI 2024

GUI:

    ++++++++++++++++++++++++++++ app ++++++++++++++++++++++++++++
    -------------------------- - area - -------------------------
    | _________ d1 _____________  ___________ d2 ________________|
    ||                          ||                               |
    || p1 (plot)    p2 (plot)   ||          (Buttons)            |
    ||                          ||                               |
    ||                          ||_______________________________|
    ||                          |____________ d3 ________________|
    ||                          ||                               |
    ||                          ||                               |
    ||                          ||          (Text)               |
    ||                          ||                               |
    ||__________________________||_______________________________|
    |------------------------------------------------------------|

USER INTERACTIONS:

    - p1 shows the data being processed with Giftwrapper
    - p2 shows the data being processed with Quickhull
    - p1 and p2 run one after another so execution time measurements and
      the comparison of numbers of steps can be performed
    - the reset button clears the animation plots and stops any ongoing
      animation
    - run the algorithms either in GUI mode with x <= 100 points or with more 
      points --> will not be displayed in GUI, but algos will run and show
      time elapsed 
    - choose number of random generated points in textfield or load new 
      data from file (.txt) with format 
            - first line: number of points
            - second ... n: points in format x, y 

NOTES:

    - Inquiring AI-Bots to help work on this code it is likely to make use of
      the PyQt5 library on top of pyqtgraph. To keep it clean however this code
      relies on "native" pyqtgraph only for visualisations and user
      interactions without relying on PyQt5 or QtGui imports. Pyqtgraph is
      typically bundled with PySide (2 and 6)
    - For better manageability and ease of debugging  the choice was made to
      organise the code in such a way that pyqtgraph is only needed to be
      imported in one single file, and all actions related to the use of that
      library are handled in one place. As the program makes use of Event
      Buttons, the file was chosen to be where the main loop runs.

## List of libraries needed to build and run

name: ml-env
channels:

- anaconda
- conda-forge
- defaults
  dependencies:
- _libgcc_mutex=0.1=conda_forge
- _openmp_mutex=4.5=2_gnu
- blas=1.0=mkl
- bottleneck=1.3.7=py312ha883a20_0
- brotli=1.0.9=h5eee18b_8
- brotli-bin=1.0.9=h5eee18b_8
- bzip2=1.0.8=h5eee18b_6
- ca-certificates=2024.8.30=hbcca054_0
- contourpy=1.2.0=py312hdb19cb5_0
- cycler=0.11.0=pyhd3eb1b0_0
- cyrus-sasl=2.1.28=h52b45da_1
- dbus=1.13.18=hb2f20db_0
- expat=2.6.3=h6a678d5_0
- fontconfig=2.14.1=h55d465d_3
- fonttools=4.51.0=py312h5eee18b_0
- freetype=2.12.1=h4a9f257_0
- glib=2.78.4=h6a678d5_0
- glib-tools=2.78.4=h6a678d5_0
- gst-plugins-base=1.14.1=h6a678d5_1
- gstreamer=1.14.1=h5eee18b_1
- icu=73.1=h6a678d5_0
- intel-openmp=2023.1.0=hdb19cb5_46306
- joblib=1.4.2=py312h06a4308_0
- jpeg=9e=h5eee18b_3
- kiwisolver=1.4.4=py312h6a678d5_0
- krb5=1.20.1=h143b758_1
- lcms2=2.12=h3be6417_0
- ld_impl_linux-64=2.38=h1181459_1
- lerc=3.0=h295c915_0
- libbrotlicommon=1.0.9=h5eee18b_8
- libbrotlidec=1.0.9=h5eee18b_8
- libbrotlienc=1.0.9=h5eee18b_8
- libclang=14.0.6=default_hc6dbbc7_1
- libclang13=14.0.6=default_he11475f_1
- libcups=2.4.2=h2d74bed_1
- libdeflate=1.17=h5eee18b_1
- libedit=3.1.20230828=h5eee18b_0
- libffi=3.4.4=h6a678d5_1
- libgcc=14.1.0=h77fa898_1
- libgcc-ng=14.1.0=h69a702a_1
- libgfortran-ng=11.2.0=h00389a5_1
- libgfortran5=11.2.0=h1234567_1
- libglib=2.78.4=hdc74915_0
- libgomp=14.1.0=h77fa898_1
- libiconv=1.16=h5eee18b_3
- libllvm14=14.0.6=hdb19cb5_3
- libpng=1.6.39=h5eee18b_0
- libpq=12.17=hdbd6064_0
- libstdcxx=14.1.0=hc0a3c3a_1
- libstdcxx-ng=14.1.0=h4852527_1
- libtiff=4.5.1=h6a678d5_0
- libuuid=1.41.5=h5eee18b_0
- libwebp-base=1.3.2=h5eee18b_0
- libxcb=1.15=h7f8727e_0
- libxkbcommon=1.0.1=h097e994_2
- libxml2=2.13.1=hfdd30dd_2
- lz4-c=1.9.4=h6a678d5_1
- matplotlib=3.9.2=py312h06a4308_0
- matplotlib-base=3.9.2=py312h66fe004_0
- mkl=2023.1.0=h213fc3f_46344
- mkl-service=2.4.0=py312h5eee18b_1
- mkl_fft=1.3.10=py312h5eee18b_0
- mkl_random=1.2.7=py312h526ad5a_0
- mysql=5.7.24=h721c034_2
- ncurses=6.4=h6a678d5_0
- numexpr=2.8.7=py312hf827012_0
- numpy=1.26.4=py312hc5e2394_0
- numpy-base=1.26.4=py312h0da6c21_0
- openjpeg=2.5.2=he7f1fd0_0
- openssl=3.3.2=hb9d3cd8_0
- packaging=24.1=py312h06a4308_0
- pandas=2.2.2=py312h526ad5a_0
- pcre2=10.42=hebb0a14_1
- pillow=10.4.0=py312h5eee18b_0
- pip=24.2=py312h06a4308_0
- ply=3.11=py312h06a4308_1
- pybind11-abi=5=hd3eb1b0_0
- pyparsing=3.1.2=py312h06a4308_0
- pyqt=5.15.10=py312h6a678d5_0
- pyqt5-sip=12.13.0=py312h5eee18b_0
- pyqtgraph=0.13.1=py312h06a4308_0
- python=3.12.4=h5148396_1
- python-dateutil=2.9.0post0=py312h06a4308_2
- python-tzdata=2023.3=pyhd3eb1b0_0
- pytz=2024.1=py312h06a4308_0
- qt-main=5.15.2=h53bd1ea_10
- readline=8.2=h5eee18b_0
- scikit-learn=1.5.1=py312h526ad5a_0
- scipy=1.13.1=py312hc5e2394_0
- setuptools=72.1.0=py312h06a4308_0
- sip=6.7.12=py312h6a678d5_0
- six=1.16.0=pyhd3eb1b0_1
- sqlite=3.45.3=h5eee18b_0
- tbb=2021.8.0=hdb19cb5_0
- threadpoolctl=3.5.0=py312he106c6f_0
- tk=8.6.14=h39e8969_0
- tornado=6.4.1=py312h5eee18b_0
- tzdata=2024a=h04d1e81_0
- unicodedata2=15.1.0=py312h5eee18b_0
- wheel=0.43.0=py312h06a4308_0
- xz=5.4.6=h5eee18b_1
- zlib=1.2.13=h5eee18b_1
- zstd=1.5.5=hc292b87_2
- pip:
    - astroid==3.2.4
    - dill==0.3.8
    - flake8==7.1.1
    - greenlet==3.0.3
    - isort==5.13.2
    - jedi==0.19.1
    - mccabe==0.7.0
    - msgpack==1.0.8
    - parso==0.8.4
    - platformdirs==4.3.2
    - pycodestyle==2.12.1
    - pyflakes==3.2.0
    - pylint==3.2.7
    - pynvim==0.5.0
    - tomlkit==0.13.2
      prefix: /home/salome/miniconda3/envs/ml-env
