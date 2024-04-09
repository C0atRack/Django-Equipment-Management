void setBuildStatus(String job_context, String state) {
  step([
      $class: "GitHubCommitStatusSetter",
      reposSource: [$class: "ManuallyEnteredRepositorySource", url: "https://github.com/C0atRack/Django-Equipment-Management"],
      contextSource: [$class: "ManuallyEnteredCommitContextSource", context: job_context],
      errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
      statusResultSource: [ $class: "ConditionalStatusResultSource", results: [[$class: "AnyBuildResult", state: state]] ]
  ]);
}

pipeline {
    agent { label 'Alpine Python Container'}
    stages{
        stage('Clone repo'){
            steps{
                updateGitlabCommitStatus name: 'Clone repo', state: 'running'
                checkout scm
            }
            post{
                success {
                    updateGitlabCommitStatus name: 'Clone repo', state: 'success'
                    setBuildStatus("Git Checkout", "SUCCESS");
                }
                failure{
                    updateGitlabCommitStatus name: 'Clone repo', state: 'failed'
                    setBuildStatus("Git Checkout", "FAIL");
                }
            }
        }
        
        stage('Setup venv'){
            steps{
                updateGitlabCommitStatus name: 'Setup Venv', state: 'running'
                sh('./pipeline_scripts/setup_venv.sh')
            }
            post{
                success {
                    updateGitlabCommitStatus name: 'Setup Venv', state: 'success'
                    setBuildStatus("Setup Venv", "SUCCESS");
                }
                failure{
                    updateGitlabCommitStatus name: 'Setup Venv', state: 'failed'
                    setBuildStatus("Setup Venv", "FAIL");
                }
            }
        }
        stage('Run testing'){
            steps{
                updateGitlabCommitStatus name: 'Running Django Tests', state: 'running'
                withCredentials([file(credentialsId: 'Testing_ENV', variable: 'ENVFILE')]){
                    sh('mv $(echo $ENVFILE | sed s/\\\'/\\\\/g) .')
                    sh('source djvenv/bin/activate; ./manage.py test --verbosity 2')
                    sh('rm \\\"$ENVFILE\\\"')
                }
            }
            post{
                success {
                    updateGitlabCommitStatus name: 'Running Django Tests', state: 'success'
                    setBuildStatus("Running Django Tests", "SUCCESS");
                }
                failure{
                    updateGitlabCommitStatus name: 'Running Django Tests', state: 'failed'
                    setBuildStatus("Running Django Tests", "FAIL");
                }
            }
        }
    }
}
