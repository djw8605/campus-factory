#!/bin/sh


# Untar the executables
tar xzf glideinExec.tar.gz

# Make the temporary directory
local_dir=`mktemp -d -t -p /state/partition1/tmp/`

export CONDOR_CONFIG=`pwd`/glidein_condor_config
export _condor_CONDOR_HOST=ff-grid.unl.edu
export _condor_GLIDEIN_HOST=ff-grid.unl.edu
export _condor_LOCAL_DIR=$local_dir
export _condor_SBIN=`pwd`/glideinExec
export _condor_CONDOR_ADMIN=dweitzel@ff.unl.edu
export _condor_NUM_CPUS=1
export _condor_UID_DOMAIN=ff.unl.edu
export _condor_FILESYSTEM_DOMAIN=ff.unl.edu
export _condor_MAIL=/bin/mail
export _condor_STARTD_NOCLAIM_SHUTDOWN=1200


if [ -e `pwd`/user_job_wrapper.sh ]
then
export _condor_USER_JOB_WRAPPER=`pwd`/user_job_wrapper.sh
fi

./glideinExec/glidein_startup -dyn -f


rm -rf $local_dir

