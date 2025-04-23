package main

import "net"

type Tester struct {
	Namespaces []Namespace `yaml:"namespaces"`
	Pods       []Pod       `yaml:"pods"`
	Tests      []Test      `yaml:"tests"`
}

type Namespace struct {
	Name   string            `yaml:"name"`
	Labels map[string]string `yaml:"labels"`
}

type Pod struct {
	Name      string            `yaml:"name"`
	Namespace string            `yaml:"namespace"`
	Labels    map[string]string `yaml:"labels"`
	Ports     []Port            `yaml:"ports"`
	IP        net.IP            `yaml:"ip"`
}

type Port struct {
	Name     string   `yaml:"name"`
	Protocol Protocol `yaml:"protocol"`
	Port     uint16   `yaml:"port"`
}

type Protocol int8

const (
	TCP Protocol = iota
	UDP
	SCTP
)

type Test struct {
	Name        string       `yaml:"name"`
	Policies    []string     `yaml:"policies"`
	Connections []Connection `yaml:"connections"`
}

type Connection struct {
	Name   string `yaml:"name"`
	From   Node   `yaml:"from"`
	To     Node   `yaml:"to"`
	Result Result `yaml:"result"`
}

type Node struct {
	Pod  string `yaml:"pod"`
	IP   string `yaml:"ip"`
	Host string `yaml:"host"`
	Port uint16 `yaml:"port"`
}

type Result bool

const (
	Denied Result = false
	Allowed
)

func main() {

}
