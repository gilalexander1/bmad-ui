'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Play,
  Pause,
  Square,
  Users,
  User,
  CheckCircle2,
  Clock,
  AlertCircle,
  Terminal,
  FileText,
  Code,
  Database,
  Zap,
  Activity,
  Settings,
  Eye
} from 'lucide-react'

interface Agent {
  id: string
  name: string
  role: string
  status: 'idle' | 'active' | 'completed' | 'error' | 'waiting'
  progress: number
  currentTask: string
  icon: any
}

interface WorkflowStep {
  id: string
  name: string
  description: string
  status: 'pending' | 'active' | 'completed' | 'error'
  agents: string[]
  progress: number
  estimatedTime: string
  outputs: string[]
}

export default function BMADWorkflow() {
  const [isRunning, setIsRunning] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [agents, setAgents] = useState<Agent[]>([
    {
      id: 'pm',
      name: 'PROJECT MANAGER',
      role: 'Mission Coordinator',
      status: 'idle',
      progress: 0,
      currentTask: 'Awaiting deployment orders',
      icon: Users
    },
    {
      id: 'architect',
      name: 'SYSTEM ARCHITECT',
      role: 'Infrastructure Designer',
      status: 'idle',
      progress: 0,
      currentTask: 'Standing by for blueprint generation',
      icon: Settings
    },
    {
      id: 'dev',
      name: 'CORE DEVELOPER',
      role: 'Code Implementation Specialist',
      status: 'idle',
      progress: 0,
      currentTask: 'Ready for coding operations',
      icon: Code
    },
    {
      id: 'qa',
      name: 'QUALITY ASSURANCE',
      role: 'Testing and Validation Unit',
      status: 'idle',
      progress: 0,
      currentTask: 'Monitoring for quality gates',
      icon: CheckCircle2
    }
  ])

  const [workflowSteps, setWorkflowSteps] = useState<WorkflowStep[]>([
    {
      id: 'planning',
      name: 'MISSION PLANNING',
      description: 'Requirements analysis and project scope definition',
      status: 'pending',
      agents: ['pm', 'architect'],
      progress: 0,
      estimatedTime: '2-4 minutes',
      outputs: ['Project Requirements Document', 'Technical Architecture']
    },
    {
      id: 'architecture',
      name: 'SYSTEM ARCHITECTURE',
      description: 'Technical design and infrastructure planning',
      status: 'pending',
      agents: ['architect', 'dev'],
      progress: 0,
      estimatedTime: '3-6 minutes',
      outputs: ['System Architecture Document', 'Database Schema', 'API Specifications']
    },
    {
      id: 'development',
      name: 'CODE DEPLOYMENT',
      description: 'Implementation of core functionality and features',
      status: 'pending',
      agents: ['dev', 'architect'],
      progress: 0,
      estimatedTime: '8-15 minutes',
      outputs: ['Source Code', 'Configuration Files', 'Documentation']
    },
    {
      id: 'testing',
      name: 'QUALITY VALIDATION',
      description: 'Testing, validation, and performance optimization',
      status: 'pending',
      agents: ['qa', 'dev'],
      progress: 0,
      estimatedTime: '4-8 minutes',
      outputs: ['Test Results', 'Quality Report', 'Performance Metrics']
    },
    {
      id: 'deployment',
      name: 'MISSION DEPLOYMENT',
      description: 'Final deployment and system activation',
      status: 'pending',
      agents: ['pm', 'dev', 'qa'],
      progress: 0,
      estimatedTime: '2-3 minutes',
      outputs: ['Deployment Package', 'System Status', 'Go-Live Confirmation']
    }
  ])

  const [terminalLogs, setTerminalLogs] = useState<string[]>([
    '> BMAD Workflow System Initialized',
    '> Agent Team Assembly Complete',
    '> Awaiting Mission Parameters...'
  ])

  const startWorkflow = () => {
    setIsRunning(true)
    addLog('> MISSION DEPLOYMENT INITIATED')
    addLog('> All agents reporting for duty')
    
    // Simulate workflow progression
    simulateWorkflow()
  }

  const pauseWorkflow = () => {
    setIsRunning(false)
    addLog('> MISSION PAUSED - Agents holding position')
  }

  const stopWorkflow = () => {
    setIsRunning(false)
    setCurrentStep(0)
    resetWorkflow()
    addLog('> MISSION TERMINATED - All agents returning to base')
  }

  const addLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString()
    setTerminalLogs(prev => [...prev, `${timestamp} ${message}`].slice(-10))
  }

  const resetWorkflow = () => {
    setAgents(prev => prev.map(agent => ({
      ...agent,
      status: 'idle' as const,
      progress: 0,
      currentTask: 'Awaiting deployment orders'
    })))
    setWorkflowSteps(prev => prev.map(step => ({
      ...step,
      status: 'pending' as const,
      progress: 0
    })))
  }

  const simulateWorkflow = () => {
    // This would connect to real backend WebSocket in production
    let step = 0
    const interval = setInterval(() => {
      if (!isRunning || step >= workflowSteps.length) {
        clearInterval(interval)
        if (step >= workflowSteps.length) {
          addLog('> MISSION COMPLETED SUCCESSFULLY')
          addLog('> All objectives achieved - Standing down')
        }
        return
      }

      // Update current step
      setCurrentStep(step)
      setWorkflowSteps(prev => prev.map((s, i) => ({
        ...s,
        status: i === step ? 'active' : i < step ? 'completed' : 'pending',
        progress: i === step ? Math.floor(Math.random() * 100) : i < step ? 100 : 0
      })))

      // Update agents
      const currentStepData = workflowSteps[step]
      setAgents(prev => prev.map(agent => ({
        ...agent,
        status: currentStepData.agents.includes(agent.id) ? 'active' : 'idle',
        progress: currentStepData.agents.includes(agent.id) ? Math.floor(Math.random() * 100) : 0,
        currentTask: currentStepData.agents.includes(agent.id) 
          ? `Working on ${currentStepData.name.toLowerCase()}`
          : 'Standing by'
      })))

      addLog(`> ${currentStepData.name} phase initiated`)
      addLog(`> Agents ${currentStepData.agents.join(', ').toUpperCase()} deployed`)

      step++
    }, 5000) // 5 seconds per step for demo
  }

  useEffect(() => {
    const interval = setInterval(() => {
      if (isRunning) {
        // Simulate real-time progress updates
        setWorkflowSteps(prev => prev.map((step, i) => 
          i === currentStep && step.status === 'active' 
            ? { ...step, progress: Math.min(100, step.progress + Math.floor(Math.random() * 10)) }
            : step
        ))
        
        setAgents(prev => prev.map(agent => 
          agent.status === 'active'
            ? { ...agent, progress: Math.min(100, agent.progress + Math.floor(Math.random() * 5)) }
            : agent
        ))
      }
    }, 1000)

    return () => clearInterval(interval)
  }, [isRunning, currentStep])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-matrix-green border-matrix-green'
      case 'completed': return 'text-emerald-400 border-emerald-400'
      case 'error': return 'text-red-400 border-red-400'
      case 'waiting': return 'text-yellow-400 border-yellow-400'
      default: return 'text-gray-400 border-gray-600'
    }
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Command Center Header */}
      <motion.div
        className="glass-heavy p-6 border border-matrix-green/30"
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold font-mono text-matrix-green tracking-wider flex items-center space-x-3">
              <Eye className="w-8 h-8" />
              <span>BMAD WORKFLOW CONTROL</span>
            </h1>
            <p className="font-mono text-sm text-gray-400 mt-2">
              Mission Status: {isRunning ? 'ACTIVE DEPLOYMENT' : 'STANDBY'} • 
              Step {currentStep + 1} of {workflowSteps.length}
            </p>
          </div>

          <div className="flex items-center space-x-4">
            <motion.button
              onClick={startWorkflow}
              disabled={isRunning}
              className={`flex items-center space-x-2 px-6 py-3 font-mono text-sm transition-all ${
                isRunning ? 'glass text-gray-500' : 'glass-button text-matrix-green hover:bg-matrix-green/20'
              }`}
              whileHover={!isRunning ? { scale: 1.05 } : {}}
              whileTap={!isRunning ? { scale: 0.95 } : {}}
              animate={!isRunning ? {
                boxShadow: [
                  "0 0 20px rgba(0,255,65,0.3)",
                  "0 0 30px rgba(0,255,65,0.5)",
                  "0 0 20px rgba(0,255,65,0.3)"
                ]
              } : {}}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <Play className="w-4 h-4" />
              <span>DEPLOY</span>
            </motion.button>

            <motion.button
              onClick={pauseWorkflow}
              disabled={!isRunning}
              className={`flex items-center space-x-2 px-6 py-3 font-mono text-sm transition-all ${
                !isRunning ? 'glass text-gray-500' : 'glass-button text-yellow-400 hover:bg-yellow-400/20'
              }`}
              whileHover={isRunning ? { scale: 1.05 } : {}}
              whileTap={isRunning ? { scale: 0.95 } : {}}
            >
              <Pause className="w-4 h-4" />
              <span>HOLD</span>
            </motion.button>

            <motion.button
              onClick={stopWorkflow}
              className="flex items-center space-x-2 px-6 py-3 font-mono text-sm glass-button text-red-400 hover:bg-red-400/20 transition-all"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Square className="w-4 h-4" />
              <span>ABORT</span>
            </motion.button>
          </div>
        </div>
      </motion.div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Workflow Steps */}
        <div className="lg:col-span-2 space-y-4">
          <div className="glass p-6 border border-matrix-green/30">
            <h2 className="font-mono text-lg font-bold text-matrix-green mb-6 flex items-center space-x-2">
              <Activity className="w-5 h-5" />
              <span>MISSION PHASES</span>
            </h2>

            <div className="space-y-4">
              {workflowSteps.map((step, index) => (
                <motion.div
                  key={step.id}
                  className={`glass p-4 border-l-4 transition-all ${
                    step.status === 'active' ? 'border-l-matrix-green bg-matrix-green/5' :
                    step.status === 'completed' ? 'border-l-emerald-400 bg-emerald-400/5' :
                    step.status === 'error' ? 'border-l-red-400 bg-red-400/5' :
                    'border-l-gray-600'
                  }`}
                  animate={step.status === 'active' ? {
                    boxShadow: [
                      "0 0 10px rgba(0,255,65,0.2)",
                      "0 0 20px rgba(0,255,65,0.4)",
                      "0 0 10px rgba(0,255,65,0.2)"
                    ]
                  } : {}}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className={`w-8 h-8 rounded-full border-2 flex items-center justify-center font-mono text-sm font-bold ${
                        step.status === 'active' ? 'border-matrix-green text-matrix-green' :
                        step.status === 'completed' ? 'border-emerald-400 text-emerald-400' :
                        step.status === 'error' ? 'border-red-400 text-red-400' :
                        'border-gray-600 text-gray-400'
                      }`}>
                        {index + 1}
                      </div>
                      <div>
                        <h3 className="font-mono text-sm font-bold text-matrix-green">
                          {step.name}
                        </h3>
                        <p className="font-mono text-xs text-gray-400">
                          {step.description}
                        </p>
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <div className="font-mono text-xs text-gray-400">ETA: {step.estimatedTime}</div>
                      <div className={`font-mono text-xs font-bold ${
                        step.status === 'active' ? 'text-matrix-green' :
                        step.status === 'completed' ? 'text-emerald-400' :
                        step.status === 'error' ? 'text-red-400' :
                        'text-gray-400'
                      }`}>
                        [{step.status.toUpperCase()}]
                      </div>
                    </div>
                  </div>

                  {step.status !== 'pending' && (
                    <div className="space-y-2">
                      <div className="flex justify-between text-xs font-mono text-gray-400">
                        <span>Progress</span>
                        <span>{step.progress}%</span>
                      </div>
                      <div className="w-full bg-gray-800 rounded-full h-2">
                        <motion.div
                          className={`h-2 rounded-full ${
                            step.status === 'completed' ? 'bg-emerald-400' :
                            step.status === 'error' ? 'bg-red-400' :
                            'bg-matrix-green'
                          }`}
                          style={{ width: `${step.progress}%` }}
                          initial={{ width: 0 }}
                          animate={{ width: `${step.progress}%` }}
                          transition={{ duration: 0.5 }}
                        />
                      </div>
                    </div>
                  )}

                  {step.outputs.length > 0 && step.status === 'completed' && (
                    <div className="mt-3 pt-3 border-t border-gray-700">
                      <div className="font-mono text-xs text-gray-400 mb-2">Outputs Generated:</div>
                      <div className="flex flex-wrap gap-2">
                        {step.outputs.map((output, i) => (
                          <span
                            key={i}
                            className="px-2 py-1 bg-emerald-400/20 text-emerald-400 text-xs font-mono rounded border border-emerald-400/30"
                          >
                            {output}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          </div>
        </div>

        {/* Agent Status & Terminal */}
        <div className="space-y-6">
          {/* Agent Status */}
          <div className="glass p-6 border border-matrix-green/30">
            <h2 className="font-mono text-lg font-bold text-matrix-green mb-6 flex items-center space-x-2">
              <Users className="w-5 h-5" />
              <span>AGENT STATUS</span>
            </h2>

            <div className="space-y-4">
              {agents.map((agent) => {
                const IconComponent = agent.icon
                return (
                  <motion.div
                    key={agent.id}
                    className={`glass p-4 border transition-all ${getStatusColor(agent.status)}`}
                    animate={agent.status === 'active' ? {
                      borderColor: [
                        "rgba(0,255,65,0.3)",
                        "rgba(0,255,65,0.8)",
                        "rgba(0,255,65,0.3)"
                      ]
                    } : {}}
                    transition={{ duration: 2, repeat: Infinity }}
                  >
                    <div className="flex items-center space-x-3 mb-2">
                      <IconComponent className={`w-5 h-5 ${getStatusColor(agent.status).split(' ')[0]}`} />
                      <div className="flex-1">
                        <div className="font-mono text-sm font-bold text-matrix-green">
                          {agent.name}
                        </div>
                        <div className="font-mono text-xs text-gray-400">
                          {agent.role}
                        </div>
                      </div>
                      <motion.div
                        className={`w-3 h-3 rounded-full ${
                          agent.status === 'active' ? 'bg-matrix-green' :
                          agent.status === 'completed' ? 'bg-emerald-400' :
                          agent.status === 'error' ? 'bg-red-400' :
                          'bg-gray-600'
                        }`}
                        animate={agent.status === 'active' ? {
                          opacity: [1, 0.3, 1]
                        } : {}}
                        transition={{ duration: 1, repeat: Infinity }}
                      />
                    </div>

                    <div className="font-mono text-xs text-gray-300 mb-3">
                      {agent.currentTask}
                    </div>

                    {agent.status !== 'idle' && (
                      <div className="space-y-1">
                        <div className="flex justify-between text-xs font-mono text-gray-400">
                          <span>Progress</span>
                          <span>{agent.progress}%</span>
                        </div>
                        <div className="w-full bg-gray-800 rounded-full h-1.5">
                          <motion.div
                            className={`h-1.5 rounded-full ${
                              agent.status === 'completed' ? 'bg-emerald-400' :
                              agent.status === 'error' ? 'bg-red-400' :
                              'bg-matrix-green'
                            }`}
                            style={{ width: `${agent.progress}%` }}
                            initial={{ width: 0 }}
                            animate={{ width: `${agent.progress}%` }}
                            transition={{ duration: 0.5 }}
                          />
                        </div>
                      </div>
                    )}
                  </motion.div>
                )
              })}
            </div>
          </div>

          {/* Terminal */}
          <div className="glass border border-matrix-green/30">
            <div className="flex items-center justify-between p-4 border-b border-matrix-green/30">
              <div className="flex items-center space-x-2">
                <Terminal className="w-4 h-4 text-matrix-green" />
                <span className="font-mono text-sm font-bold text-matrix-green">SYSTEM CONSOLE</span>
              </div>
              <motion.div
                className="flex space-x-1"
                animate={{ opacity: [1, 0.5, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <div className="w-2 h-2 rounded-full bg-red-500"></div>
                <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
                <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
              </motion.div>
            </div>

            <div className="p-4 bg-black/50 h-64 overflow-y-auto">
              <div className="font-mono text-xs space-y-1">
                <AnimatePresence>
                  {terminalLogs.map((log, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="text-matrix-green"
                    >
                      {log}
                    </motion.div>
                  ))}
                </AnimatePresence>
                <motion.span
                  animate={{ opacity: [1, 0, 1] }}
                  transition={{ duration: 1, repeat: Infinity }}
                  className="text-matrix-green"
                >
                  █
                </motion.span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}