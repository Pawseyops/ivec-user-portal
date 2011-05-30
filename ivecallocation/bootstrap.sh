#!/bin/sh

#
# Its a sample script, tested only to the point of running manage.py runserver_plus
#
# You need to have python dev header files installed for mx.DateTime to install

VPYTHON_DIR='mypython'
VIRTUALENV='virtualenv-1.6.1'
VIRTUALENV_TARBALL='virtualenv-1.6.1.tar.gz'

# only install if we dont already exist
if [ ! -d $VPYTHON_DIR ]
then
    echo -e '\n\nNo virtual python dir, lets create one\n\n'

    # only install virtual env if its not hanging around
    if [ ! -d $VIRTUALENV ]
    then
        echo -e '\n\nNo virtual env, creating\n\n'
  
        # only download the tarball if needed
        if [ ! -f $VIRTUALENV_TARBALL ]
        then
            wget http://pypi.python.org/packages/source/v/virtualenv/$VIRTUALENV_TARBALL
        fi

        # build virtualenv
        tar zxvf $VIRTUALENV_TARBALL
        cd $VIRTUALENV
        python setup.py build
        cd ..

    fi
       
    # create a virtual python in the current directory
    python $VIRTUALENV/build/lib*/virtualenv.py --no-site-packages $VPYTHON_DIR

    # we need mx.DateTime for psycopg2
    #./$VPYTHON_DIR/bin/easy_install egenix-mx-base

    # install all the eggs in this app
    ./$VPYTHON_DIR/bin/easy_install eggs/*


    # hack activate to set some environment we need
    # this version nukes the python path
    # hard coded yebife.settings, better version would determine this programatically
    echo "PROJECT_DIRECTORY=`pwd`;" >>  $VPYTHON_DIR/bin/activate
    #echo "DJANGO_SETTINGS_MODULE=yabife.settings"  >>  $VPYTHON_DIR/bin/activate
    #echo "PYTHONPATH='$PYTHONPATH:/usr/local/etc/ccgapps/'" >>  $VPYTHON_DIR/bin/activate
    echo "PYTHONPATH=/usr/local/etc/ccgapps/" >>  $VPYTHON_DIR/bin/activate

    echo "export PROJECT_DIRECTORY DJANGO_SETTINGS_MODULE PYTHONPATH" >>  $VPYTHON_DIR/bin/activate

fi


# tell the (l)user how to activate this python install
echo -e "\n\nTo activate this python install, type the following at the prompt:\n\nsource $VPYTHON_DIR/bin/activate\n\n"
