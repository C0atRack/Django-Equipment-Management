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
                }
                failure{
                    updateGitlabCommitStatus name: 'Clone repo', state: 'failed'
                }
            }
        }
        
        stage('Setup venv'){
            steps{
                updateGitlabCommitStatus name: 'Testing run', state: 'running'
                sh('echo Hello world!')
            }
            post{
                success {
                    updateGitlabCommitStatus name: 'Testing run', state: 'success'
                }
                failure{
                    updateGitlabCommitStatus name: 'Testing run', state: 'failed'
                }
            }
        }
    }
}
