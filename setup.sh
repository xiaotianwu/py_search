export PY_SEARCH_ROOT=`pwd`
echo $PY_SEARCH_ROOT
export PYTHONPATH=$PYTHONPATH:$PY_SEARCH_ROOT
alias createut=$PY_SEARCH_ROOT/tools/CreateUTTemplate.py
