# -*- coding: utf-8 -*-
from sqlalchemy import *
from datetime import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from config import *


def createSession(filename):
    engine = create_engine('sqlite:///'+database_dir+database_file, echo = True)
    metadata = MetaData(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    return session


Base = declarative_base()

class Komand(Base):
    __tablename__ = 'komand'
    komand_id = Column(Integer, primary_key = True)
    komand_zadan = Column(String())
    komand_addr = Column(String())
    komand_org = Column(String())
    komand_start = Column(Date())
    komand_end = Column(Date())
    komand_cos = Column(String())
    def __init__(self, komand_zadan, komand_addr, 
            komand_org, komand_start, komand_end, komand_cos):
        self.komand_id = None
        self.komand_zadan = komand_zadan
        self.komand_addr = komand_addr
        self.komand_org = komand_org
        self.komand_start = komand_start
        self.komand_end = komand_end
        self.komand_cos = komand_cos
    def __repr__(self):
        return "<Командировка('%s', '%s')>" % (self.id, self.komand_zadan)

class ServRecord(Base): 
    __tablename__ = 'serv_recods'
    record_id = Column(Integer,primary_key = True)
    record_kom_id = Column(Integer, ForeignKey('komand.komand_id'))
    record_num = Column(Integer)
    record_date = Column(Date())
    record_fio = Column(String())
    record_tabnum = Column(Integer)
    record_str_podr = Column(String())
    record_dolg = Column(String())
    record_addr = Column(String())
    record_org = Column(String())
    record_start = Column(Date())
    record_end = Column(Date())
    record_zadan = Column(String())
    record_osn = Column(String())
    record_ruk_str_otpr_dolg = Column(String())
    record_ruk_str_otpr_fio = Column(String())
    record_ruk_str_prin_dolg = Column(String())
    record_ruk_str_prin_fio = Column(String())
    record_ruk_org_dolg = Column(String())
    record_ruk_org_fio = Column(String())

    def __init__(self, record_kom_id, record_num, record_date, record_fio, record_tabnum,
        record_str_podr, record_dolg, record_addr, record_org, record_start,
        record_end, record_zadan, record_osn, record_ruk_str_otpr_dolg, 
        record_ruk_str_otpr_fio, 
        record_ruk_str_prin_dolg, record_ruk_str_prin_fio, 
        record_ruk_org_dolg, record_ruk_org_fio):
        self.record_id = None
        self.record_kom_id = record_kom_id
        self.record_num = record_num
        self.record_date = record_date
        self.record_fio = record_fio
        self.record_tabnum = record_tabnum
        self.record_str_podr = record_str_podr
        self.record_dolg = record_dolg
        self.record_addr = record_addr
        self.record_org = record_org
        self.record_start = record_start
        self.record_end = record_end
        self.record_zadan = record_zadan
        self.record_osn = record_osn
        self.record_ruk_str_otpr_dolg = record_ruk_str_otpr_dolg
        self.record_ruk_str_otpr_fio = record_ruk_str_otpr_fio
        self.record_ruk_str_prin_dolg = record_ruk_str_prin_dolg
        self.record_ruk_str_prin_fio = record_ruk_str_prin_fio
        self.record_ruk_org_dolg = record_ruk_org_dolg
        self.record_ruk_org_fio = record_ruk_org_fio

    def __repr__(self):
        return "<Служ. записка №'%s'>" % (self.record_num)

class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer,primary_key = True)
    group_short_name = Column(String())
    group_long_name = Column(String())
    def __init__(self, group_short_name, group_long_name):
        self.group_id = None
        self.group_short_name = group_short_name
        self.group_long_name = group_long_name
    def __repr__(self):
        return "<Group('%s', '%s')>" % (self.group_id, self.group_long_name)

class Dept(Base):
    __tablename__ = 'depts'
    dept_id = Column(Integer, primary_key = True)
    dept_short_name = Column(String())
    dept_long_name = Column(String())
    def __init__(self, dept_short_name, dept_long_name):
        self.dept_id = None
        self.dept_long_name = dept_long_name
        self.dept_short_name = dept_short_name
    def __repr__(self):
        return u"<Подразделение ('%s', '%s')>" % (self.dept_id, self.dept_short_name)

class Position(Base):
    __tablename__ = 'positions'
    pos_id = Column(Integer, primary_key = True)
    pos_name = Column(String())
    pos_short_name = Column(String())
    group = Column(Integer, ForeignKey('groups.group_id'))
    dept = Column(Integer, ForeignKey('depts.dept_id'))
    employee = Column(Integer)
    def __init__(self, pos_name, pos_short_name, group, dept):
        self.pos_id = None
        self.pos_name = pos_name
        self.pos_short_name = pos_short_name
        self.group = group.group_id
        self.dept = dept.dept_id
        self.employee = 0;
    def __repr__(self):
        return "<Position('%s', group'%s')>" % (self.pos_name, self.group)

class Employee(Base):
    __tablename__ = 'employees'
    empl_id = Column(Integer, primary_key = True)
    family = Column(String())
    name = Column(String())
    sname = Column(String())
    born_date = Column(Date())
    start_pos = Column(Date())
    position = Column(Integer)
    tab_num = Column(Integer)
    def __init__(self, family, name, sname, position, tab_num):
        self.empl_id = None
        self.family = family
        self.name = name
        self.sname = sname
        self.position = position
        self.tab_num = tab_num
    def __repr__(self):
        return "<Employee('%s', '%s', '%s')>" % (self.family, self.name, self.sname)


