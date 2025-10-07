-- Create "todos" table
CREATE TABLE `todos` (
  `id` integer NOT NULL,
  `title` varchar NOT NULL,
  `complete` boolean NOT NULL,
  PRIMARY KEY (`id`)
);
