*** Settings ***
Library             SSHLibrary
Documentation       Resource file for demo purposes.
...                 This resource is only used in an example and it doesn't do anything useful.

*** Variables ***
${HOST}             172.16.99.34
${USERNAME}         liutao
${PASSWORD}         mx960-123

*** keywords ***
Open Connection And Log In
    Open Connection     ${HOST}
    Login               ${USERNAME}     ${PASSWORD}

BGP Health Check
    [Documentation]     Check BGP State
    ${output}=          Execute Command     show bgp neighbor
    Should Contain      ${output}           State: Established

NAT Public IP
    [Documentation]     Check If Tranlated Public IP address is in the VRF route-table.
    ${output}=          Execute Command     show route table l3vpn-service-39.inet.0
    Should Contain      ${output}           101.234.59.59/32   *[Static/1]

NAT Ping from CE
    [Documentation]     Ping from CE side to Remote CE IP address.
    ${output}=          Execute Command     ping 172.162.39.2 logical-system CE-l3vpn-loopback count 2
    Should Contain      ${output}           64 bytes from 172.162.39.2

NAT Session Validation
    [Documentation]     Validating NAT session of ICMP sent From Local CE.
    ${output}=          Execute Command     show services sessions service-set MS-OFFICE-SERVICE-SET-59 extensive
    Should Contain      ${output}           ICMP       172.162.39.2        ->   101.234.59.59

Remove Test Files And Close Connections
    Close All Connections