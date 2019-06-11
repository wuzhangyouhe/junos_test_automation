*** Settings ***
Library             SSHLibrary
Resource            resources.robot
Suite Setup         Open Connection And Log In
Suite Teardown      Close All Connections
Documentation       Start Service Validation in SQL lab.

*** Test Cases ***
Initial Tests
    BGP Health Check

NAT Service Tests
    NAT Public IP
    NAT Ping from CE
    NAT Session Validation