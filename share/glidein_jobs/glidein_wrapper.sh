#!/bin/sh


# Untar the executables
tar xzf glideinExec.tar.gz

# Make the temporary directory
local_dir=`mktemp -d -t -p /state/partition1/tmp/`

# All late-binding configurations
export CONDOR_CONFIG=`pwd`/glidein_condor_config
export _condor_LOCAL_DIR=$local_dir
export _condor_SBIN=`pwd`/glideinExec


if [ -e `pwd`/user_job_wrapper.sh ]
then
export _condor_USER_JOB_WRAPPER=`pwd`/user_job_wrapper.sh
fi

./glideinExec/glidein_startup -dyn -f


rm -rf $local_dir

