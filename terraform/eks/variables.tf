variable "region" {
  type        = "string"
  description = "AWS region"
}


variable m4_x_spot_price {
  type        = map
  description = "Spot Instance price based on region"
  default = {
    us-west-1 = "0.080"
    eu-west-1 = "0.289"
  }
}

variable m4_2x_spot_price {
  type        = map
  description = "Spot Instance price based on region"
  default = {
    us-west-1 = "0.140"
    eu-west-1 = "0.569"
  }
}