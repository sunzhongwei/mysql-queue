-- CREATE DATABASE IF NOT EXISTS mysql_queue;

DROP TABLE task_queue;

CREATE TABLE IF NOT EXISTS task_queue (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	msg_id INT NOT NULL,
	`status` VARCHAR(20) DEFAULT 'unprocess' NOT NULL,	
	`worker_id` INT DEFAULT 0 NOT NULL,
	created_at DATETIME NOT NULL,
	finished_at DATETIME 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Init test data 
INSERT INTO task_queue 
	(msg_id, created_at) VALUES 
	(1, "2015-11-06 16:48:00"),
	(2, "2015-11-06 16:49:00"),
	(3, "2015-11-06 16:49:00"),
	(4, "2015-11-06 16:49:00"),
	(5, "2015-11-06 16:49:00"),
	(6, "2015-11-06 16:49:00"),
	(7, "2015-11-06 16:49:00");
