import { Outlet, useNavigate } from 'react-router-dom'
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from '@mui/material'
import DashboardIcon from '@mui/icons-material/Dashboard'
import TaskIcon from '@mui/icons-material/Task'
import KeyIcon from '@mui/icons-material/Key'
import { useAuth } from '../contexts/AuthContext'
import { useEffect } from 'react'

const drawerWidth = 240

export default function Layout() {
  const { isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login')
    }
  }, [isAuthenticated, navigate])

  if (!isAuthenticated) {
    return null
  }

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
      >
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            AWS Automation Platform
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          <Typography
            variant="body2"
            onClick={logout}
            sx={{ cursor: 'pointer' }}
          >
            Logout
          </Typography>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            <ListItem disablePadding>
              <ListItemButton onClick={() => navigate('/dashboard')}>
                <ListItemIcon>
                  <DashboardIcon />
                </ListItemIcon>
                <ListItemText primary="Dashboard" />
              </ListItemButton>
            </ListItem>
            <ListItem disablePadding>
              <ListItemButton onClick={() => navigate('/tasks')}>
                <ListItemIcon>
                  <TaskIcon />
                </ListItemIcon>
                <ListItemText primary="Tasks" />
              </ListItemButton>
            </ListItem>
            <ListItem disablePadding>
              <ListItemButton onClick={() => navigate('/aws-credentials')}>
                <ListItemIcon>
                  <KeyIcon />
                </ListItemIcon>
                <ListItemText primary="AWS Credentials" />
              </ListItemButton>
            </ListItem>
          </List>
        </Box>
      </Drawer>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          bgcolor: 'background.default',
          p: 3,
        }}
      >
        <Toolbar />
        <Container maxWidth="lg">
          <Outlet />
        </Container>
      </Box>
    </Box>
  )
}
