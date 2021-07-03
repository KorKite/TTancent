# Database "focus" 생성
create database focus

# 만든 Database 선택
\c focus

# Userinfo 테이블 생성
create table USERINFO(
    UserId bit(12) primary key,
    UserName bit varying(10) not null,
    UserPassword bit varying(24) not null,
    IsProf boolean not null,
    UserEmail bit varying(24) UNIQUE
);

# class 테이블 생성 (수업 관련 내용)
create table class (
    classid bit(10) primary key,
    generatorid bit(10) constraint userid references userinfo,
    classname bit varying(24) unique not null,
    isOpen boolean
);

# user_class_rel 테이블 생성 (유저의 수업별, 그냥 점수 기록)
create table user_class_rel(
    id bit(10) primary key,
    userid bit(10) constraint userid references userinfo,
    classid bit(10) constraint classid references class,
    score bigint not null,
    createdAt date not null
);


#  user_class_avg 테이블 생성 (수업의 평균 점수 저장)
create table user_class_avg(
    id bit(10) primary key,
    userid bit(10) constraint userid references userinfo,
    classid bit(10) constraint classid references class,
    avg bigint not null,
    when_gen bit varying(10) not null
);