APP="$0"
COMMAND=$1
DIR="$2"

if [ "$1" = "" ]; then
 echo "
 To deploy, run:
 ./deploy --install [ .deploy location ]
 
 To update already existing deployment, run:
 ./deploy --update [ .deploy location ]
 
 It will run copy, replace and update-s2...
 
 Partial deployment options:
 ./deploy --begin        Run begin script
 ./deploy --copy         Copy files to /tmp
 ./deploy --replace      Replace the old files
 ./deploy --finish       Run the finish script
 ./deploy --update-s2    Run the update script, only
 
 If the location where the .deploy file isn't specified, deploy.sh will assume
 it's in the current directory."
 exit
fi

# clean up the location string
if [ "$DIR" = "" ]; then
        DIR="$( cd "$( dirname "$0" )" && pwd )"
elif [ "$DIR" = "./" ]; then
        DIR="$( cd "$( dirname "$0" )" && pwd )"
else
        DIR=$(echo "$DIR" | sed -e 's/\/$//g')
fi

# full commands
if [ "$COMMAND" = "--install" ]; then
        echo "Initiating executing of full deploying sequence..." 
        $APP --begin
        $APP --copy
        $APP --replace
        $APP --finish
        echo "Deployment is done"
        exit
elif [ "$COMMAND" = "--update" ]; then
        echo "Initiating executing of update sequence..." 
        $APP --copy
        $APP --replace
        $APP --update-s2
        echo "Update is done"
        exit
elif [ "$COMMAND" = "--help" ]; then
	$APP
	exit
fi

# get user info
USER=$(cat /etc/deploy.conf | sed -e '/^$/ d' -e '/^[#].*/ d' -e '/server/,$ d' -e 's/^user//g' -e 's/[ \t]/,/g')
USER_NAME=$(echo "$USER" | cut -d',' -f2)
USER_KEY=$(echo "$USER" | cut -d',' -f3)

# get server list
SERVERS=$(cat /etc/deploy.conf | sed -e '/^$/ d' -e '/^[#u].*/ d')

# get file list
FILES=$(cat /$DIR/.deploy | sed -e '/^$/ d' -e '/^[#].*/ d' -e '/BEGIN\:/,$ d')

# get begin script
SCRIPT_BEGIN=$(cat /$DIR/.deploy | sed -e '1,/BEGIN\:/ d' -e '/FINISH\:/,$ d')

# get finish script
SCRIPT_FINISH=$(cat /$DIR/.deploy | sed -e '1,/FINISH\:/ d' -e '/UPDATE\:/,$ d')

# get update script
SCRIPT_UPDATE=$(cat /$DIR/.deploy | sed -e '1,/UPDATE\:/ d')

# let's do the job...
GROUP=no
GROUP_NAME=all
FILE_GROUP=no
FILE_GROUP_NAME=all
for server in $SERVERS
do
        if [ "$server" = "server" ]; then
                GROUP=yes
        elif [ "$GROUP" = "yes" ]; then
                GROUP_NAME=$server
                GROUP=no
        else
                LF=$(echo '\n ')
                if [ "$COMMAND" = "--begin" ]; then
                        echo "Running script at $server($GROUP_NAME)..."
                        SHEBANG="#!/bin/sh${LF}DEPLOY_GROUP=${GROUP_NAME}"
                        SCRIPT="${SHEBANG}${LF}${SCRIPT_BEGIN}"
                        echo "/bin/sh ${SCRIPT}" | ssh -i $USER_KEY $USER_NAME@$server
                elif [ "$COMMAND" = "--finish" ]; then
                        SHEBANG="#!/bin/sh${LF}DEPLOY_GROUP=${GROUP_NAME}"
                        SCRIPT="${SHEBANG}${LF}${SCRIPT_FINISH}"
                        echo "/bin/sh ${SCRIPT}" | ssh -i $USER_KEY $USER_NAME@$server
                elif [ "$COMMAND" = "--update-s2" ]; then
                        SHEBANG="#!/bin/sh${LF}DEPLOY_GROUP=${GROUP_NAME}"
                        SCRIPT="${SHEBANG}${LF}${SCRIPT_UPDATE}"
                        echo "/bin/sh ${SCRIPT}" | ssh -i $USER_KEY $USER_NAME@$server
                else
                for file in $FILES
                do
                        if [ "$file" = "file" ]; then
                                FILE_GROUP=yes
                        elif [ "$FILE_GROUP" = "yes" ]; then
                                FILE_GROUP_NAME=$file
                                FILE_GROUP=no
                        elif [ "$FILE_GROUP_NAME" = "$GROUP_NAME" ]; then
                                filename=$(basename $file)
                                echo " * $filename\t=> $server ($GROUP_NAME)"
                                if [ "$COMMAND" = "--copy" ]; then
                                        # copy files
                                        scp -i $USER_KEY $file $USER_NAME@$server:/tmp/$filename >> /dev/null
                                elif [ "$COMMAND" = "--replace" ]; then
                                        # move files    
                                        echo "sudo mv /tmp/$filename $file" | ssh -i $USER_KEY $USER_NAME@$server
                                else
                                        echo "Wrong options"
                                fi
                        fi
                done
                fi
        fi
done

exit