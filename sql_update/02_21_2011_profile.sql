BEGIN;
-- Application: project
-- Model: Project
ALTER TABLE `project_project`
  ADD `profile_id` integer;
CREATE INDEX `project_project_profile_id_idx`
  ON `project_project` (`profile_id`);
COMMIT;

