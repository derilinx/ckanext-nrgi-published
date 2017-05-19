#!/usr/bin/env bash

# Triggers automatic deploy for certain branches. As this is an extension for the
# main CKAN repo it triggers the build of the main CKAN repo.
#
# Uses Shippable env variables:
# - BRANCH

set -e

elementIn () {
  local e
  for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 0; done
  return 1
}

# Automatic deploy allowed for these branches only.
DEPLOY_BRANCHES=("master" "staging")

if ! elementIn "$BRANCH" "${DEPLOY_BRANCHES[@]}" ;
then
  echo "Skiping deploy as branch is not allowed for automatic deploy"
fi

# Id of the Shippable project containing the deploy script.
CKAN_ROOT_PROJECT_ID=591d863568194107000b6287

# Accomodate for non-standard branch naming on triggered project
if [ "$BRANCH" == "master" ]
then
  BRANCH="nrgi"
fi


# Trigger Shippable to run the deploy project and pass the current project name, branch and latest commit
STATUS=$(
  curl -s\
  -H "Authorization: apiToken $API_TOKEN"\
  -H "Content-Type: application/json"\
  -d "{\"branchName\":\"$BRANCH\"}"\
  "https://api.shippable.com/projects/$CKAN_ROOT_PROJECT_ID/newBuild"
)
echo "$STATUS"

if [[ "$STATUS" == *"runId"* ]]
then
  echo "Deploy triggered successfully";
  exit 0
else
  echo "Failed to trigger deploy.";
  exit 1
fi
