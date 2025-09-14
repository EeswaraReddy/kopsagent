# Sample Terraform configuration for deploying the knowledgeops-agent

provider "postgresql" {
  host     = "localhost"
  port     = 5432
  username = "your_username"
  password = "your_password"
  database = "knowledgeops_db"
}

resource "postgresql_database" "knowledgeops_db" {
  name = "knowledgeops_db"
}

resource "postgresql_role" "knowledgeops_user" {
  name     = "knowledgeops_user"
  password = "your_password"
  login    = true
}

resource "postgresql_grant" "knowledgeops_grant" {
  database = postgresql_database.knowledgeops_db.name
  role     = postgresql_role.knowledgeops_user.name
  privileges = ["ALL"]
}

resource "docker_container" "knowledgeops_container" {
  image = "your_docker_image"
  name  = "knowledgeops-agent"
  
  ports {
    internal = 80
    external = 8080
  }

  environment = {
    DATABASE_URL = "postgresql://${postgresql_role.knowledgeops_user.name}:${postgresql_role.knowledgeops_user.password}@${postgresql_database.knowledgeops_db.name}:5432/knowledgeops_db"
  }
}