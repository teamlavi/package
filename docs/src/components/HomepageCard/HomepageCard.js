import React from 'react'
import { Card, CardContent, CardActions, Button, Typography } from "@mui/material"


export default function HomepageCard({ title, subtitle, path }) {
    return <Card sx={{maxWidth: 275}}>
    <CardContent>
      <Typography variant="h5" component="div">
        {title}
      </Typography>
      <Typography sx={{ mb: 1.5, fontSize: "16px" }} color="text.secondary">
        {subtitle}
      </Typography>
    </CardContent>
    <CardActions>
      <Button href={path} size="small">Learn More</Button>
    </CardActions>
  </Card>
}