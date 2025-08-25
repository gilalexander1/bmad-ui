'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  ChevronRight, 
  ChevronLeft, 
  Rocket, 
  Settings, 
  Users, 
  Code, 
  Database,
  Globe,
  Zap,
  CheckCircle,
  AlertTriangle,
  Target,
  Cpu
} from 'lucide-react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

interface ProjectCreationWizardProps {
  onComplete: () => void
}

const projectSchema = z.object({
  name: z.string().min(1, 'Project name is required'),
  description: z.string().min(10, 'Description must be at least 10 characters'),
  type: z.enum(['greenfield-fullstack', 'brownfield-fullstack', 'greenfield-ui', 'brownfield-ui']),
  techStack: z.object({
    frontend: z.string(),
    backend: z.string(),
    database: z.string(),
  }),
  agentTeam: z.string(),
  objectives: z.array(z.string()).min(1, 'At least one objective is required'),
})

type ProjectData = z.infer<typeof projectSchema>

export default function ProjectCreationWizard({ onComplete }: ProjectCreationWizardProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [projectData, setProjectData] = useState<Partial<ProjectData>>({
    objectives: []
  })

  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm<ProjectData>({
    resolver: zodResolver(projectSchema),
    defaultValues: projectData,
    mode: 'onChange'
  })

  const steps = [
    {
      id: 'basic',
      title: 'MISSION PARAMETERS',
      subtitle: 'Define primary objectives and classification',
      icon: Target,
      color: 'from-emerald-400 to-cyan-500'
    },
    {
      id: 'tech',
      title: 'TECHNICAL STACK',
      subtitle: 'Select deployment architecture and frameworks',
      icon: Cpu,
      color: 'from-cyan-400 to-blue-500'
    },
    {
      id: 'team',
      title: 'AGENT DEPLOYMENT',
      subtitle: 'Configure agent team composition',
      icon: Users,
      color: 'from-blue-400 to-purple-500'
    },
    {
      id: 'confirm',
      title: 'MISSION BRIEFING',
      subtitle: 'Review and initialize deployment sequence',
      icon: CheckCircle,
      color: 'from-purple-400 to-pink-500'
    }
  ]

  const techOptions = {
    frontend: ['Next.js', 'React', 'Vue.js', 'Angular', 'Svelte'],
    backend: ['FastAPI', 'Node.js', 'Django', 'Flask', 'Express'],
    database: ['PostgreSQL', 'MongoDB', 'MySQL', 'SQLite', 'Redis']
  }

  const agentTeams = [
    { id: 'team-fullstack', name: 'Full-Stack Squadron', description: 'Complete development team with all specialties' },
    { id: 'team-frontend', name: 'UI Strike Team', description: 'Frontend-focused rapid deployment unit' },
    { id: 'team-backend', name: 'Core Systems Unit', description: 'Backend and infrastructure specialists' },
    { id: 'team-minimal', name: 'Stealth Ops', description: 'Minimal viable team for rapid prototyping' }
  ]

  const projectTypes = [
    { 
      id: 'greenfield-fullstack', 
      name: 'NEW TERRITORY FULL ASSAULT',
      description: 'Complete new project with frontend and backend',
      icon: Rocket
    },
    { 
      id: 'brownfield-fullstack', 
      name: 'OCCUPIED ZONE ENHANCEMENT',
      description: 'Enhance existing full-stack project',
      icon: Settings
    },
    { 
      id: 'greenfield-ui', 
      name: 'INTERFACE ESTABLISHMENT',
      description: 'New frontend-only project',
      icon: Globe
    },
    { 
      id: 'brownfield-ui', 
      name: 'UI SECTOR UPGRADE',
      description: 'Improve existing user interface',
      icon: Code
    }
  ]

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const addObjective = () => {
    const objectives = watch('objectives') || []
    setValue('objectives', [...objectives, ''])
  }

  const removeObjective = (index: number) => {
    const objectives = watch('objectives') || []
    setValue('objectives', objectives.filter((_, i) => i !== index))
  }

  const updateObjective = (index: number, value: string) => {
    const objectives = watch('objectives') || []
    const newObjectives = [...objectives]
    newObjectives[index] = value
    setValue('objectives', newObjectives)
  }

  const onSubmit = (data: ProjectData) => {
    console.log('Mission Parameters Confirmed:', data)
    onComplete()
  }

  const stepVariants = {
    hidden: { opacity: 0, x: 100 },
    visible: { 
      opacity: 1, 
      x: 0,
      transition: {
        type: "spring",
        damping: 20,
        stiffness: 100
      }
    },
    exit: { 
      opacity: 0, 
      x: -100,
      transition: {
        duration: 0.3
      }
    }
  }

  const renderStepContent = () => {
    const currentStepData = steps[currentStep]

    switch (currentStepData.id) {
      case 'basic':
        return (
          <div className="space-y-8">
            <div className="space-y-6">
              <div>
                <label className="block font-mono text-sm text-matrix-green mb-2 tracking-wide">
                  [ MISSION CODENAME ]
                </label>
                <input
                  {...register('name')}
                  className="form-input w-full text-lg font-mono"
                  placeholder="Enter project identifier..."
                />
                {errors.name && (
                  <motion.p 
                    className="text-red-400 text-xs font-mono mt-1"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                  >
                    ⚠ {errors.name.message}
                  </motion.p>
                )}
              </div>

              <div>
                <label className="block font-mono text-sm text-matrix-green mb-2 tracking-wide">
                  [ MISSION DESCRIPTION ]
                </label>
                <textarea
                  {...register('description')}
                  className="form-input w-full h-32 resize-none font-mono text-sm"
                  placeholder="Describe mission objectives and scope..."
                />
                {errors.description && (
                  <motion.p 
                    className="text-red-400 text-xs font-mono mt-1"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                  >
                    ⚠ {errors.description.message}
                  </motion.p>
                )}
              </div>

              <div>
                <label className="block font-mono text-sm text-matrix-green mb-4 tracking-wide">
                  [ OPERATION TYPE ]
                </label>
                <div className="grid md:grid-cols-2 gap-4">
                  {projectTypes.map((type) => {
                    const IconComponent = type.icon
                    return (
                      <motion.div
                        key={type.id}
                        className={`glass cursor-pointer p-6 border-2 transition-all ${
                          watch('type') === type.id 
                            ? 'border-matrix-green bg-matrix-green/10' 
                            : 'border-gray-600 hover:border-matrix-green/50'
                        }`}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => setValue('type', type.id as any)}
                      >
                        <div className="flex items-start space-x-4">
                          <IconComponent className="w-8 h-8 text-matrix-green flex-shrink-0 mt-1" />
                          <div>
                            <h3 className="font-mono text-sm font-bold text-matrix-green mb-1">
                              {type.name}
                            </h3>
                            <p className="text-xs text-gray-300 font-mono leading-relaxed">
                              {type.description}
                            </p>
                          </div>
                        </div>
                      </motion.div>
                    )
                  })}
                </div>
                {errors.type && (
                  <motion.p 
                    className="text-red-400 text-xs font-mono mt-2"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                  >
                    ⚠ {errors.type.message}
                  </motion.p>
                )}
              </div>
            </div>
          </div>
        )

      case 'tech':
        return (
          <div className="space-y-8">
            <div className="grid md:grid-cols-3 gap-6">
              {Object.entries(techOptions).map(([category, options]) => (
                <div key={category}>
                  <label className="block font-mono text-sm text-matrix-green mb-4 tracking-wide">
                    [ {category.toUpperCase()} FRAMEWORK ]
                  </label>
                  <div className="space-y-2">
                    {options.map((option) => (
                      <motion.div
                        key={option}
                        className={`glass cursor-pointer p-3 border transition-all font-mono text-sm ${
                          watch(`techStack.${category as keyof typeof techOptions}`) === option
                            ? 'border-matrix-green bg-matrix-green/10 text-matrix-green'
                            : 'border-gray-600 hover:border-matrix-green/50 text-gray-300'
                        }`}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => setValue(`techStack.${category as keyof typeof techOptions}`, option)}
                      >
                        <div className="flex items-center justify-between">
                          <span>{option}</span>
                          {watch(`techStack.${category as keyof typeof techOptions}`) === option && (
                            <motion.div
                              initial={{ scale: 0 }}
                              animate={{ scale: 1 }}
                            >
                              <CheckCircle className="w-4 h-4 text-matrix-green" />
                            </motion.div>
                          )}
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div>
              <label className="block font-mono text-sm text-matrix-green mb-4 tracking-wide">
                [ MISSION OBJECTIVES ]
              </label>
              <div className="space-y-3">
                {(watch('objectives') || []).map((objective, index) => (
                  <motion.div
                    key={index}
                    className="flex space-x-3"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                  >
                    <input
                      className="form-input flex-1 font-mono text-sm"
                      placeholder={`Objective ${index + 1}...`}
                      value={objective}
                      onChange={(e) => updateObjective(index, e.target.value)}
                    />
                    <motion.button
                      type="button"
                      onClick={() => removeObjective(index)}
                      className="glass-button p-3 text-red-400 hover:text-red-300"
                      whileHover={{ scale: 1.1 }}
                      whileTap={{ scale: 0.9 }}
                    >
                      ✕
                    </motion.button>
                  </motion.div>
                ))}
                <motion.button
                  type="button"
                  onClick={addObjective}
                  className="glass-button p-3 w-full font-mono text-sm text-matrix-green border-dashed border-matrix-green/50 hover:border-matrix-green"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  + ADD OBJECTIVE
                </motion.button>
              </div>
            </div>
          </div>
        )

      case 'team':
        return (
          <div className="space-y-6">
            <label className="block font-mono text-sm text-matrix-green mb-4 tracking-wide">
              [ AGENT TEAM SELECTION ]
            </label>
            <div className="grid md:grid-cols-2 gap-6">
              {agentTeams.map((team) => (
                <motion.div
                  key={team.id}
                  className={`glass cursor-pointer p-6 border-2 transition-all ${
                    watch('agentTeam') === team.id
                      ? 'border-matrix-green bg-matrix-green/10'
                      : 'border-gray-600 hover:border-matrix-green/50'
                  }`}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setValue('agentTeam', team.id)}
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h3 className="font-mono text-sm font-bold text-matrix-green">
                        {team.name}
                      </h3>
                      {watch('agentTeam') === team.id && (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                        >
                          <CheckCircle className="w-5 h-5 text-matrix-green" />
                        </motion.div>
                      )}
                    </div>
                    <p className="text-xs text-gray-300 font-mono leading-relaxed">
                      {team.description}
                    </p>
                    <div className="flex items-center space-x-2">
                      <Users className="w-4 h-4 text-cyan-400" />
                      <span className="text-xs font-mono text-cyan-400">
                        READY FOR DEPLOYMENT
                      </span>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        )

      case 'confirm':
        return (
          <div className="space-y-8">
            <div className="glass-heavy p-6 border border-matrix-green/30">
              <h3 className="font-mono text-lg font-bold text-matrix-green mb-6 text-center">
                [ MISSION BRIEFING CONFIRMATION ]
              </h3>
              
              <div className="grid md:grid-cols-2 gap-8">
                <div className="space-y-4">
                  <div>
                    <span className="font-mono text-xs text-gray-400">CODENAME:</span>
                    <p className="font-mono text-matrix-green font-bold">{watch('name') || 'UNDEFINED'}</p>
                  </div>
                  <div>
                    <span className="font-mono text-xs text-gray-400">OPERATION:</span>
                    <p className="font-mono text-matrix-green">
                      {projectTypes.find(t => t.id === watch('type'))?.name || 'UNSPECIFIED'}
                    </p>
                  </div>
                  <div>
                    <span className="font-mono text-xs text-gray-400">AGENT TEAM:</span>
                    <p className="font-mono text-matrix-green">
                      {agentTeams.find(t => t.id === watch('agentTeam'))?.name || 'UNASSIGNED'}
                    </p>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <span className="font-mono text-xs text-gray-400">TECH STACK:</span>
                    <div className="font-mono text-xs text-matrix-green space-y-1">
                      <div>FRONTEND: {watch('techStack.frontend') || 'UNDEFINED'}</div>
                      <div>BACKEND: {watch('techStack.backend') || 'UNDEFINED'}</div>
                      <div>DATABASE: {watch('techStack.database') || 'UNDEFINED'}</div>
                    </div>
                  </div>
                  <div>
                    <span className="font-mono text-xs text-gray-400">OBJECTIVES:</span>
                    <div className="font-mono text-xs text-matrix-green space-y-1">
                      {(watch('objectives') || []).map((obj, i) => (
                        <div key={i}>• {obj || `Objective ${i + 1}`}</div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <motion.div
              className="text-center p-6 glass border border-yellow-400/30"
              animate={{
                borderColor: [
                  "rgba(251, 191, 36, 0.3)",
                  "rgba(251, 191, 36, 0.8)",
                  "rgba(251, 191, 36, 0.3)"
                ]
              }}
              transition={{
                duration: 2,
                repeat: Infinity
              }}
            >
              <AlertTriangle className="w-8 h-8 text-yellow-400 mx-auto mb-3" />
              <p className="font-mono text-sm text-yellow-400">
                [ WARNING: MISSION DEPLOYMENT IS IRREVERSIBLE ]
              </p>
              <p className="font-mono text-xs text-gray-400 mt-2">
                Confirm all parameters before proceeding with agent deployment
              </p>
            </motion.div>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Progress Header */}
      <motion.div
        className="glass-heavy p-6 mb-8"
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold font-mono text-matrix-green tracking-wide">
              PROJECT INITIALIZATION SEQUENCE
            </h1>
            <p className="font-mono text-sm text-gray-400 mt-2">
              Step {currentStep + 1} of {steps.length} • {steps[currentStep].subtitle}
            </p>
          </div>
          <motion.div
            className="text-right"
            animate={{
              opacity: [1, 0.5, 1]
            }}
            transition={{
              duration: 2,
              repeat: Infinity
            }}
          >
            <div className="font-mono text-xs text-gray-400">SYSTEM STATUS</div>
            <div className="font-mono text-sm text-matrix-green">[ ONLINE ]</div>
          </motion.div>
        </div>

        {/* Step Progress */}
        <div className="flex items-center space-x-4">
          {steps.map((step, index) => {
            const IconComponent = step.icon
            return (
              <div key={step.id} className="flex items-center">
                <motion.div
                  className={`flex items-center justify-center w-12 h-12 rounded-lg border-2 ${
                    index === currentStep
                      ? 'border-matrix-green bg-matrix-green/20 text-matrix-green'
                      : index < currentStep
                      ? 'border-emerald-400 bg-emerald-400/20 text-emerald-400'
                      : 'border-gray-600 text-gray-400'
                  }`}
                  animate={index === currentStep ? {
                    boxShadow: [
                      "0 0 10px rgba(0,255,65,0.3)",
                      "0 0 20px rgba(0,255,65,0.6)",
                      "0 0 10px rgba(0,255,65,0.3)"
                    ]
                  } : {}}
                  transition={{
                    duration: 2,
                    repeat: Infinity
                  }}
                >
                  <IconComponent className="w-6 h-6" />
                </motion.div>
                {index < steps.length - 1 && (
                  <div className={`w-8 h-0.5 mx-4 ${
                    index < currentStep ? 'bg-emerald-400' : 'bg-gray-600'
                  }`} />
                )}
              </div>
            )
          })}
        </div>
      </motion.div>

      {/* Step Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={currentStep}
          variants={stepVariants}
          initial="hidden"
          animate="visible"
          exit="exit"
          className="glass-heavy p-8 min-h-[500px]"
        >
          <div className="text-center mb-8">
            <motion.div
              className={`w-16 h-16 mx-auto rounded-lg bg-gradient-to-br ${steps[currentStep].color} flex items-center justify-center mb-4`}
              animate={{
                rotate: [0, 5, -5, 0],
                scale: [1, 1.1, 1]
              }}
              transition={{
                duration: 4,
                repeat: Infinity
              }}
            >
              {React.createElement(steps[currentStep].icon, { 
                className: "w-8 h-8 text-white" 
              })}
            </motion.div>
            <h2 className="text-xl font-bold font-mono text-matrix-green tracking-wider">
              {steps[currentStep].title}
            </h2>
          </div>

          <form onSubmit={handleSubmit(onSubmit)}>
            {renderStepContent()}

            {/* Navigation */}
            <div className="flex items-center justify-between mt-12 pt-8 border-t border-matrix-green/20">
              <motion.button
                type="button"
                onClick={prevStep}
                disabled={currentStep === 0}
                className={`flex items-center space-x-2 px-6 py-3 font-mono text-sm transition-all ${
                  currentStep === 0
                    ? 'text-gray-500 cursor-not-allowed'
                    : 'glass-button text-gray-300 hover:text-white'
                }`}
                whileHover={currentStep > 0 ? { scale: 1.05 } : {}}
                whileTap={currentStep > 0 ? { scale: 0.95 } : {}}
              >
                <ChevronLeft className="w-4 h-4" />
                <span>PREVIOUS</span>
              </motion.button>

              {currentStep < steps.length - 1 ? (
                <motion.button
                  type="button"
                  onClick={nextStep}
                  className="flex items-center space-x-2 px-6 py-3 font-mono text-sm glass-button text-matrix-green hover:bg-matrix-green/20"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <span>PROCEED</span>
                  <ChevronRight className="w-4 h-4" />
                </motion.button>
              ) : (
                <motion.button
                  type="submit"
                  className="flex items-center space-x-2 px-8 py-3 font-mono text-sm font-bold bg-gradient-to-r from-matrix-green to-emerald-400 text-black rounded-lg"
                  whileHover={{ 
                    scale: 1.05,
                    boxShadow: "0 0 30px rgba(0,255,65,0.5)"
                  }}
                  whileTap={{ scale: 0.95 }}
                  animate={{
                    boxShadow: [
                      "0 0 20px rgba(0,255,65,0.3)",
                      "0 0 40px rgba(0,255,65,0.6)",
                      "0 0 20px rgba(0,255,65,0.3)"
                    ]
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity
                  }}
                >
                  <Rocket className="w-5 h-5" />
                  <span>DEPLOY MISSION</span>
                </motion.button>
              )}
            </div>
          </form>
        </motion.div>
      </AnimatePresence>
    </div>
  )
}