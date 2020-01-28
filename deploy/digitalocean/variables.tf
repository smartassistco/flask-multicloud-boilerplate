variable "do_token" {
  type        = string
  description = "Your DigitalOcean API token"
  default     = "80b07dde85ab9b08cdd8b9fa2771ac4ebb60084e5e612abc3493e243938fe3f0"
}

variable "ssh_fingerprint" {
  type        = string
  description = "Your SSH key fingerprint"
  default     = ""
}

variable "pub_key" {
  type        = string
  description = "The path to your public SSH key"
  default     = "~/.ssh/id_rsa.pub"
}

variable "pvt_key" {
  type        = string
  description = "The path to your private SSH key"
  default     = "~/.ssh/id_rsa"
}

