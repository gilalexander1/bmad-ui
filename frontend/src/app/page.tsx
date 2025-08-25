'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Rocket, Zap, Users, Terminal, FileText, Settings } from 'lucide-react'
import ProjectCreationWizard from '@/components/ProjectCreationWizard'
import BMADWorkflow from '@/components/BMADWorkflow'
import CosmicDashboard from '@/components/CosmicDashboard'

type ViewType = 'dashboard' | 'create-project' | 'workflow'

export default function HomePage() {
  const [currentView, setCurrentView] = useState<ViewType>('dashboard')

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.8,
        staggerChildren: 0.2
      }
    }
  }

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: "spring",
        damping: 20,
        stiffness: 100
      }
    }
  }

  const renderCurrentView = () => {
    switch (currentView) {
      case 'create-project':
        return (
          <motion.div
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.5 }}
          >
            <ProjectCreationWizard onComplete={() => setCurrentView('workflow')} />
          </motion.div>
        )
      case 'workflow':
        return (
          <motion.div
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.5 }}
          >
            <BMADWorkflow />
          </motion.div>
        )
      default:
        return (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <CosmicDashboard onNavigate={setCurrentView} />
          </motion.div>
        )
    }
  }

  return (
    <div className="min-h-screen p-4 md:p-8">
      {/* Navigation Header */}
      <motion.header
        className="glass mb-8 p-4 md:p-6"
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        <nav className="flex items-center justify-between">
          <motion.div
            className="flex items-center space-x-4"
            whileHover={{ scale: 1.05 }}
          >
            <div className="w-10 h-10 bg-gradient-to-br from-matrix-green to-cosmic-500 rounded-lg flex items-center justify-center">
              <Rocket className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl md:text-3xl font-bold text-gradient">
                BMAD UI
              </h1>
              <p className="text-sm text-gray-300">
                Enhanced Agent Methodology Interface v2.0
              </p>
            </div>
          </motion.div>

          <div className="flex items-center space-x-2 md:space-x-4">
            <motion.button
              onClick={() => setCurrentView('dashboard')}
              className={`glass-button px-3 py-2 md:px-4 md:py-2 rounded-lg text-sm font-medium transition-all ${
                currentView === 'dashboard' ? 'bg-matrix-green/20 text-matrix-green' : 'text-gray-300 hover:text-white'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Settings className="w-4 h-4 md:mr-2" />
              <span className="hidden md:inline">Dashboard</span>
            </motion.button>

            <motion.button
              onClick={() => setCurrentView('create-project')}
              className={`glass-button px-3 py-2 md:px-4 md:py-2 rounded-lg text-sm font-medium transition-all ${
                currentView === 'create-project' ? 'bg-matrix-green/20 text-matrix-green' : 'text-gray-300 hover:text-white'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <FileText className="w-4 h-4 md:mr-2" />
              <span className="hidden md:inline">Create</span>
            </motion.button>

            <motion.button
              onClick={() => setCurrentView('workflow')}
              className={`glass-button px-3 py-2 md:px-4 md:py-2 rounded-lg text-sm font-medium transition-all ${
                currentView === 'workflow' ? 'bg-matrix-green/20 text-matrix-green' : 'text-gray-300 hover:text-white'
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Terminal className="w-4 h-4 md:mr-2" />
              <span className="hidden md:inline">Workflow</span>
            </motion.button>
          </div>
        </nav>
      </motion.header>

      {/* Main Content Area */}
      <motion.main
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="container mx-auto max-w-7xl"
      >
        {renderCurrentView()}
      </motion.main>

      {/* Floating Action Elements */}
      <motion.div
        className="fixed bottom-6 right-6 flex flex-col space-y-3"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 1, type: "spring" }}
      >
        <motion.div
          className="glass w-12 h-12 rounded-full flex items-center justify-center cursor-pointer cosmic-pulse"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setCurrentView('create-project')}
        >
          <Zap className="w-6 h-6 text-matrix-green" />
        </motion.div>

        <motion.div
          className="glass w-12 h-12 rounded-full flex items-center justify-center cursor-pointer"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setCurrentView('workflow')}
        >
          <Users className="w-6 h-6 text-cosmic-400" />
        </motion.div>
      </motion.div>

      {/* Status Bar */}
      <motion.div
        className="fixed bottom-0 left-0 right-0 glass-heavy p-3 bg-black/20"
        initial={{ y: 100 }}
        animate={{ y: 0 }}
        transition={{ delay: 1.2 }}
      >
        <div className="flex items-center justify-between text-xs text-gray-400">
          <div className="flex items-center space-x-4">
            <span className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-matrix-green rounded-full animate-pulse"></div>
              <span>System Online</span>
            </span>
            <span>BMAD Core v4.0</span>
            <span>Agent Teams Ready</span>
          </div>
          <div className="flex items-center space-x-4">
            <span>{new Date().toLocaleTimeString()}</span>
            <span className="matrix-text">█</span>
          </div>
        </div>
      </motion.div>
    </div>
  )
}