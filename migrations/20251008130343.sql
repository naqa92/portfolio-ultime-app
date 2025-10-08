-- Create "todos" table
CREATE TABLE "todos" (
  "id" serial NOT NULL,
  "title" character varying(100) NOT NULL,
  "complete" boolean NOT NULL,
  PRIMARY KEY ("id")
);
