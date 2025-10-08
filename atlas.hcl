# Atlas configuration for SQLAlchemy migrations
#
# This configuration allows Atlas to manage database migrations
# for the TodoList application using SQLAlchemy models.

# Define the external schema source from SQLAlchemy models
data "external_schema" "sqlalchemy" {
  program = [
    "atlas-provider-sqlalchemy",
    "--path", "./app/models",
    "--dialect", "postgresql"
  ]
}

# PostgreSQL environment
env "postgres" {
  # Use SQLAlchemy models as the source of truth
  src = data.external_schema.sqlalchemy.url
  
  # Development database for schema diffing
  dev = "docker://postgres/16/dev?search_path=public"
  
  # Migration files directory
  migration {
    dir = "file://migrations"
  }
  
  # Format for migration files
  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}
