基于[blog_xtg](https://github.com/xtg20121013/blog_xtg)进行开发。

增加功能：

1. 添加功能使用\``` code \```进行代码编写，原项目写博客的时不能使用```进行代码高亮

2.添加评论的邮箱认证功能

如果需要使用这个功能，需要在原版本中的数据库添加一张表

```
CREATE TABLE `commentCode` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(64) NOT NULL,
  `code` int(11) NOT NULL,
  `update_time` int(18) NOT NULL DEFAULT '0' COMMENT '更新的时间戳',
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8
```
