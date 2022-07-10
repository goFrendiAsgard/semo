set -e

__OLD_IFS="${IFS}"
IFS=$'\n'

_DEPLOYMENT_DIR_PATH="zaruba-tasks/make/${_ZRB_APP_NAME}HelmDeployment/deploymentTemplate/ztplDeploymentDirectory"
_DEPLOYMENT_TASK_DIR_PATH="zaruba-tasks/make/${_ZRB_APP_NAME}HelmDeployment/deploymentTaskTemplate/zaruba-tasks/ztplDeploymentName"
_CHART_NAME_PARTS="$("${ZARUBA_BIN}" str split "${ZARUBA_CONFIG_CHART_NAME}" "/")"
_CHART_NAME_LENGTH="$("${ZARUBA_BIN}" list length "${_CHART_NAME_PARTS}")"
_CHART_DIR_NAME="$("${ZARUBA_BIN}" list get "${_CHART_NAME_PARTS}" "$(( ${_CHART_NAME_LENGTH} - 1 ))")"

echo "Pulling charts"

helm pull "${ZARUBA_CONFIG_CHART_NAME}" --untar --untardir "${_DEPLOYMENT_DIR_PATH}"

echo "Moving chart"
mv "${_DEPLOYMENT_DIR_PATH}/${_CHART_DIR_NAME}" "${_DEPLOYMENT_DIR_PATH}/chart"

echo "Reading values"

_CHART_VALUES="$("${ZARUBA_BIN}" yaml read "${_DEPLOYMENT_DIR_PATH}/chart/values.yaml")"

echo "Append template.env"
_TEMPLATE_ENV_SCRIPT="$(python "${_CHART_VALUE_SCRIPT}" "env" "${_CHART_VALUES}")"
echo "${_TEMPLATE_ENV_SCRIPT}" >> "${_DEPLOYMENT_DIR_PATH}/template.env"

# echo "Updating task environment"
# _JSON_ENV_MAP="$(python "${_CHART_VALUE_SCRIPT}" "json-env-map" "${_CHART_VALUES}")"
# "${ZARUBA_BIN}" task setEnvs "deployZtplDeploymentName" "${_JSON_ENV_MAP}" "${_DEPLOYMENT_TASK_DIR_PATH}/index.yaml"

echo "Updating python value"
_PYTHON_VALUE="$(python "${_CHART_VALUE_SCRIPT}" "python-value" "${_CHART_VALUES}")"

####################################################################
# read __main__.py

_MAIN_FILE_LOCATION="${_DEPLOYMENT_DIR_PATH}/__main__.py"
_MAIN_LINES="$("${ZARUBA_BIN}" lines read "${_MAIN_FILE_LOCATION}")"

####################################################################
# look for value location

_VALUE_PATTERN="values([\t ]*)=([\t ]*){}"
_VALUE_INDEX="$("${ZARUBA_BIN}" lines getIndex "${_MAIN_LINES}" "${_VALUE_PATTERN}")"
if [ "${_VALUE_INDEX}" = "-1" ]
then
    echo "Pattern not found: ${_VALUE_PATTERN}"
    exit 1
fi
_VALUE_LINE="$("${ZARUBA_BIN}" list get "${_MAIN_LINES}" "${_VALUE_INDEX}")"
_INDENTATION="$("${ZARUBA_BIN}" str getIndentation "${_VALUE_LINE}")"
_INDENTED_PYTHON_VALUE="$("${ZARUBA_BIN}" str fullIndent "${_PYTHON_VALUE}" "${_INDENTATION}")"

####################################################################
# update value

_MAIN_LINES="$("${ZARUBA_BIN}" lines replace "${_MAIN_LINES}" "${_VALUE_INDEX}" "${_INDENTED_PYTHON_VALUE}")"

####################################################################
# overwrite existing __main__.py

chmod 755 "${_MAIN_FILE_LOCATION}"
"${ZARUBA_BIN}" lines write "${_MAIN_FILE_LOCATION}" "${_MAIN_LINES}"

IFS="${__OLD_IFS}"