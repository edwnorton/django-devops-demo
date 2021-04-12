use demo;
INSERT INTO `AlertGroup`(`id`, `group`, `number`) VALUES (1, 'telgroup1', '18612345678,18612345678,18812345678');
INSERT INTO `AlertGroup`(`id`, `group`, `number`) VALUES (2, 'telgroup2', '18612345678,18612345678');
INSERT INTO `SilenceInfo`(`id`, `alertlevel`, `silencetime`) VALUES (1, 'high', '9-22');
INSERT INTO `SilenceInfo`(`id`, `alertlevel`, `silencetime`) VALUES (2, 'critical', '0-24');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('1', 'OracleExpdpBACKUPException', 'ops', 'telgroup1', 'telgroup1', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('10', 'RedisServerDown', 'middleware', 'telgroup', 'telgroup2', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('11', 'MongoDBServerDown', 'middleware', 'telgroup', 'telgroup1', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('12', 'InfluxDBDown', 'middleware', 'telgroup', 'telgroup1', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('13', 'SwitchIfOperDown', 'ops', 'telgroup', 'telgroup2', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('14', 'NodeRestarted', 'ops', 'telgroup', 'telgroup2', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('15', 'FilesystemReadonly', 'ops', 'telgroup', 'telgroup2', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('16', 'NginxDown', 'ops', 'telgroup', 'telgroup1', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('17', 'BindDown', 'ops', 'telgroup', 'telgroup1', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('18', 'fastdfsDown', 'ops', 'telgroup', 'telgroup2', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('19', 'oracleInstanceRestart', 'ops', 'telgroup', 'telgroup2', 'critical');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('2', 'OracleRmanBACKUPException', 'ops', 'telgroup', 'telgroup2', 'critical');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('3', 'MicroserviceInstanceDown', 'app', 'telgroup', 'telgroup2', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('4', 'XSInstanceDown', 'core', 'telgroup', 'telgroup1', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('5', 'DockerDown', 'ops', 'telgroup', 'telgroup2', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('6', 'KafkaServerDown', 'middleware', 'telgroup', 'telgroup2', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('7', 'OracleServerDown', 'middleware', 'telgroup', 'telgroup2', 'critical');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('8', 'ZookeeperServerDown', 'middleware', 'telgroup', 'telgroup1', 'high');
INSERT INTO `alertsinf`(`id`, `alertname`, `alerttype`, `group`, `telgroup`, `severity`) VALUES ('9', 'MySQLServerDown', 'middleware', 'telgroup', 'telgroup1', 'critical');