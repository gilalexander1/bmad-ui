'use client'

import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'
import { 
  Rocket, 
  Zap, 
  Users, 
  Terminal, 
  FileText, 
  Settings,
  Activity,
  Cpu,
  Database,
  Wifi,
  Shield,
  Eye,
  Target
} from 'lucide-react'

interface CosmicDashboardProps {
  onNavigate: (view: 'dashboard' | 'create-project' | 'workflow') => void
}

export default function CosmicDashboard({ onNavigate }: CosmicDashboardProps) {
  const [systemTime, setSystemTime] = useState(new Date())
  const [cpuLoad, setCpuLoad] = useState(65)
  const [memoryUsage, setMemoryUsage] = useState(78)
  const [networkStatus, setNetworkStatus] = useState(true)

  useEffect(() => {
    const timer = setInterval(() => {
      setSystemTime(new Date())
      setCpuLoad(Math.floor(Math.random() * 40) + 50)
      setMemoryUsage(Math.floor(Math.random() * 30) + 60)
      setNetworkStatus(Math.random() > 0.1)
    }, 2000)

    return () => clearInterval(timer)
  }, [])

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.8,
        staggerChildren: 0.1
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

  const blinkVariants = {
    animate: {
      opacity: [1, 0.3, 1],
      transition: {
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  }

  const missionControlCards = [
    {
      title: "PROJECT CREATION",
      subtitle: "Initialize New Mission",
      icon: Rocket,
      action: () => onNavigate('create-project'),
      status: "READY",
      color: "from-matrix-green to-emerald-400",
      glow: "shadow-[0_0_30px_rgba(0,255,65,0.5)]"
    },
    {
      title: "WORKFLOW EXECUTION",
      subtitle: "Agent Team Deployment",
      icon: Users,
      action: () => onNavigate('workflow'),
      status: "STANDBY",
      color: "from-cyan-400 to-blue-500",
      glow: "shadow-[0_0_30px_rgba(6,182,212,0.5)]"
    },
    {
      title: "SYSTEM TERMINAL",
      subtitle: "Direct Command Access",
      icon: Terminal,
      action: () => console.log('Terminal access'),
      status: "ACTIVE",
      color: "from-yellow-400 to-orange-500",
      glow: "shadow-[0_0_30px_rgba(251,191,36,0.5)]"
    }
  ]

  const systemMetrics = [
    { label: "CPU LOAD", value: `${cpuLoad}%`, status: cpuLoad > 80 ? "CRITICAL" : "OPTIMAL" },
    { label: "MEMORY", value: `${memoryUsage}%`, status: memoryUsage > 85 ? "WARNING" : "OPTIMAL" },
    { label: "NETWORK", value: networkStatus ? "ONLINE" : "OFFLINE", status: networkStatus ? "OPTIMAL" : "ERROR" },
    { label: "AGENTS", value: "12/12", status: "READY" }
  ]

  return (
    <motion.div
      className="space-y-8"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Mission Control Header */}
      <motion.div
        variants={itemVariants}
        className="text-center space-y-4"
      >
        <div className="flex items-center justify-center space-x-4 mb-6">
          <motion.div
            className="w-16 h-16 rounded-full bg-gradient-to-br from-matrix-green via-emerald-400 to-cyan-500 flex items-center justify-center"
            animate={{
              boxShadow: [
                "0 0 20px rgba(0,255,65,0.5)",
                "0 0 40px rgba(0,255,65,0.8)",
                "0 0 20px rgba(0,255,65,0.5)"
              ]
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            <Eye className="w-8 h-8 text-black" />
          </motion.div>
        </div>
        
        <motion.h1
          className="text-5xl md:text-7xl font-bold font-mono tracking-wider"
          style={{
            background: "linear-gradient(135deg, #00ff41, #00ffff, #0066ff)",
            backgroundSize: "200% 200%",
            backgroundClip: "text",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            textShadow: "0 0 30px rgba(0,255,65,0.5)"
          }}
          animate={{
            backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"]
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "linear"
          }}
        >
          MISSION CONTROL
        </motion.h1>
        
        <motion.p
          className="text-xl md:text-2xl font-mono text-matrix-green tracking-wide"
          variants={blinkVariants}
          animate="animate"
        >
          [ BMAD AGENT DEPLOYMENT SYSTEM ]
        </motion.p>

        <div className="font-mono text-sm text-cyan-400">
          SYSTEM TIME: {systemTime.toLocaleString()} | STATUS: OPERATIONAL
        </div>
      </motion.div>

      {/* System Status Grid */}
      <motion.div
        variants={itemVariants}
        className="grid grid-cols-2 md:grid-cols-4 gap-4"
      >
        {systemMetrics.map((metric, index) => (
          <motion.div
            key={metric.label}
            className="glass p-4 text-center border border-matrix-green/30"
            whileHover={{ 
              scale: 1.05,
              boxShadow: "0 0 25px rgba(0,255,65,0.4)"
            }}
            animate={{
              borderColor: [
                "rgba(0,255,65,0.3)",
                "rgba(0,255,65,0.6)",
                "rgba(0,255,65,0.3)"
              ]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              delay: index * 0.5
            }}
          >
            <div className="font-mono text-xs text-gray-400 mb-1">{metric.label}</div>
            <div className="font-mono text-lg font-bold text-matrix-green mb-1">
              {metric.value}
            </div>
            <div className={`font-mono text-xs ${
              metric.status === 'OPTIMAL' ? 'text-emerald-400' :
              metric.status === 'WARNING' ? 'text-yellow-400' :
              metric.status === 'CRITICAL' ? 'text-red-400' :
              metric.status === 'ERROR' ? 'text-red-500' :
              'text-cyan-400'
            }`}>
              [{metric.status}]
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Mission Control Cards */}
      <motion.div
        variants={itemVariants}
        className="grid md:grid-cols-3 gap-6"
      >
        {missionControlCards.map((card, index) => {
          const IconComponent = card.icon
          return (
            <motion.div
              key={card.title}
              className={`glass-heavy p-8 cursor-pointer border border-matrix-green/20 ${card.glow}`}
              whileHover={{ 
                scale: 1.05,
                boxShadow: "0 0 50px rgba(0,255,65,0.7)"
              }}
              whileTap={{ scale: 0.95 }}
              onClick={card.action}
              animate={{
                borderColor: [
                  "rgba(0,255,65,0.2)",
                  "rgba(0,255,65,0.8)",
                  "rgba(0,255,65,0.2)"
                ]
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                delay: index * 1
              }}
            >
              <div className="text-center space-y-6">
                <motion.div
                  className={`w-16 h-16 mx-auto rounded-lg bg-gradient-to-br ${card.color} flex items-center justify-center`}
                  animate={{
                    rotate: [0, 5, -5, 0],
                    scale: [1, 1.1, 1]
                  }}
                  transition={{
                    duration: 4,
                    repeat: Infinity,
                    delay: index * 0.7
                  }}
                >
                  <IconComponent className="w-8 h-8 text-white" />
                </motion.div>
                
                <div>
                  <h3 className="text-xl font-bold font-mono text-matrix-green tracking-wider mb-2">
                    {card.title}
                  </h3>
                  <p className="text-sm text-gray-300 font-mono mb-4">
                    {card.subtitle}
                  </p>
                  
                  <motion.div
                    className={`inline-block px-4 py-2 rounded-full border font-mono text-xs tracking-wide ${
                      card.status === 'READY' ? 'border-emerald-400 text-emerald-400' :
                      card.status === 'ACTIVE' ? 'border-yellow-400 text-yellow-400' :
                      'border-cyan-400 text-cyan-400'
                    }`}
                    variants={blinkVariants}
                    animate="animate"
                  >
                    [ {card.status} ]
                  </motion.div>
                </div>
              </div>
            </motion.div>
          )
        })}
      </motion.div>

      {/* Command Line Interface Preview */}
      <motion.div
        variants={itemVariants}
        className="glass border border-matrix-green/30 p-6"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-mono text-lg font-bold text-matrix-green">SYSTEM CONSOLE</h3>
          <motion.div
            className="flex space-x-2"
            animate={{ opacity: [1, 0.5, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
          </motion.div>
        </div>
        
        <div className="bg-black/50 p-4 rounded-lg font-mono text-sm space-y-2">
          <div className="text-matrix-green">
            <span className="text-cyan-400">bmad@control:~$</span> system status
          </div>
          <div className="text-emerald-400">✓ All systems operational</div>
          <div className="text-emerald-400">✓ Agent teams ready for deployment</div>
          <div className="text-emerald-400">✓ Network connectivity established</div>
          <div className="text-matrix-green">
            <span className="text-cyan-400">bmad@control:~$</span> 
            <motion.span
              animate={{ opacity: [1, 0, 1] }}
              transition={{ duration: 1, repeat: Infinity }}
            >
              █
            </motion.span>
          </div>
        </div>
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        variants={itemVariants}
        className="flex flex-wrap gap-4 justify-center"
      >
        {[
          { icon: Target, label: "OBJECTIVES", color: "text-red-400" },
          { icon: Shield, label: "SECURITY", color: "text-blue-400" },
          { icon: Activity, label: "MONITORING", color: "text-green-400" },
          { icon: Database, label: "DATA CORE", color: "text-purple-400" }
        ].map((action, index) => {
          const IconComponent = action.icon
          return (
            <motion.button
              key={action.label}
              className="glass px-6 py-3 font-mono text-sm border border-matrix-green/30 hover:border-matrix-green/80 transition-all"
              whileHover={{ 
                scale: 1.05,
                boxShadow: "0 0 20px rgba(0,255,65,0.4)"
              }}
              whileTap={{ scale: 0.95 }}
              animate={{
                borderColor: [
                  "rgba(0,255,65,0.3)",
                  "rgba(0,255,65,0.6)",
                  "rgba(0,255,65,0.3)"
                ]
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                delay: index * 0.8
              }}
            >
              <div className="flex items-center space-x-2">
                <IconComponent className={`w-4 h-4 ${action.color}`} />
                <span className="text-matrix-green">{action.label}</span>
              </div>
            </motion.button>
          )
        })}
      </motion.div>
    </motion.div>
  )
}