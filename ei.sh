# !/bin/sh

SCRIPT_DIR=$(cd `dirname $0` && pwd)

export PYTHONPATH=$SCRIPT_DIR/lib

echo $PYTHONPATH
easy_install -d $PYTHONPATH $@
