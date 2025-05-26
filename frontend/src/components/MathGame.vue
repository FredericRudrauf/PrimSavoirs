<template>
  <div class="game-container">
    <!-- Formulaire de démarrage -->
    <form @submit.prevent="startGame" v-if="!started" class="start-form">
      <h2 class="mb-4 text-center" style="color: #6EDCD9;">Exercices de mathématiques</h2>

      <!-- Opérations -->
      <div class="mb-3">
        <label class="form-label" style="color: #B983FF;"><strong>Opérations :</strong></label><br />
        <div class="d-flex flex-wrap gap-3">
          <div class="form-check form-check-inline" v-for="op in allOps" :key="op.value">
            <input
              class="form-check-input"
              type="checkbox"
              :id="op.value"
              :value="op.value"
              v-model="selectedOps"
            />
            <label class="form-check-label" :for="op.value">{{ op.label }}</label>
          </div>
        </div>
      </div>

      <div class="mb-3">
        <label class="form-label">Chiffres à utiliser :</label>
        <input type="text" class="form-control" v-model="digitRange" placeholder="Ex : 1-10 ou 1,2,5 ou 3" />
      </div>

      <!-- Mode de jeu -->
      <div class="mb-3">
        <label class="form-label" style="color: #B983FF;"><strong>Modes de jeu :</strong></label><br />
        <div class="d-flex flex-wrap gap-3">
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" id="fixed" value="fixed" v-model="mode" />
            <label class="form-check-label" for="fixed">Nombre de questions</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" id="timed" value="timed" v-model="mode" />
            <label class="form-check-label" for="timed">Chronométré</label>
          </div>
        </div>
      </div>

      <div class="mb-3" v-if="mode === 'fixed'">
        <label class="form-label">Nombre de questions :</label>
        <input type="number" class="form-control" v-model.number="questionCount" min="1" max="50" />
      </div>

      <div class="mb-3" v-if="mode === 'timed'">
        <label class="form-label">Durée (en secondes) :</label>
        <input type="number" class="form-control" v-model.number="duration" min="10" max="300" />
      </div>

      <div class="text-center">
        <button class="btn btn-success mt-3">Commencer</button>
      </div>
    </form>

    <!-- Affichage du calcul -->
    <div v-else-if="!gameOver" class="game-play text-center">
      <transition name="fade" mode="out-in">
        <div key="q{{ currentIndex }}" class="display-3 mb-4" v-html="renderedQuestion"></div>
      </transition>

      <input
        type="number"
        ref="answerInput"
        v-model.number="currentAnswer"
        class="form-control input-big text-center"
        @keyup.enter="validateAnswer"
      />

      <div class="mt-3">
        <button class="btn btn-primary" @click="validateAnswer">Valider</button>
        <button class="btn btn-outline-danger ms-3" @click="resetGame">
          Annuler et revenir au début
        </button>
      </div>

      <div v-if="mode === 'timed'" class="mt-4 fs-5">
        ⏱️ Temps restant : {{ timeLeft }} s
      </div>
    </div>

    <!-- Résultat -->
    <div v-else class="text-center score-display">
      <img :src="resultImage" alt="Résultat" class="mb-3 result-img" />
      <p class="fs-5 mb-4" :class="feedbackClass">{{ feedbackMessage }}</p>
      <p class="fs-3">
        Tu as eu <strong style="color:green">{{ score }}</strong> bonne(s) réponse(s) sur <strong>{{ total }}</strong>
        ({{ percent }}%).
      </p>
      <button class="btn btn-secondary" @click="resetGame">Rejouer</button>
      <div class="mt-4 text-start" style="max-width: 500px; margin: auto;">
        <h5>Erreurs :</h5>
        <ul>
          <li
            v-for="(ex, i) in exercises.filter((ex, i) => answers[i] !== undefined && answers[i] !== ex.answer)"
            :key="i"
          >
            {{ ex.question }} = {{ answers[i] }} <span class="text-danger">❌ (bonne réponse : {{ ex.answer }})</span>
          </li>
        </ul>
      </div>
    </div>
  </div> <!-- fermeture de .game-container -->
</template>

<script setup>
import { Transition } from 'vue'
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { buildMathUrl } from '../lib/api.js'

const allOps = [
  { value: 'add', label: 'Addition' },
  { value: 'sub', label: 'Soustraction' },
  { value: 'mul', label: 'Multiplication' },
  { value: 'div', label: 'Division' },
]

const colors = [
  '#FFD93D', // Jaune
  '#6EDCD9', // Turquoise
  '#F05454', // Rouge
  '#87C4FF', // Bleu pastel
  '#B983FF', // Violet
  '#06D6A0'  // Vert vif
]

const selectedOps = ref(['add'])
const mode = ref('fixed')
const questionCount = ref(5)
const duration = ref(30)

const exercises = ref([])
const answers = ref([])
const currentIndex = ref(0)
const currentAnswer = ref(null)
const timeLeft = ref(0)
const started = ref(false)
const gameOver = ref(false)
const animate = ref(true)
const answerInput = ref(null)
let timer = null

const currentQuestion = computed(() => exercises.value[currentIndex.value])

const total = computed(() => answers.value.length)
const score = computed(() =>
  answers.value.filter((val, i) => val === exercises.value[i]?.answer).length
)
const percent = computed(() =>
  total.value === 0 ? 0 : Math.round((score.value / total.value) * 100)
)

const digitRange = ref("1-10")

const feedbackMessage = computed(() => {
  if (percent.value === 100) {
    return "🧠 Parfait ! Tu es une véritable calculatrice humaine !";
  } else if (percent.value >= 75) {
    return "👏 Super ! Tu maîtrises bien tes maths.";
  } else if (percent.value >= 51) {
    return "👍 Pas mal ! Un peu de pratique et tu seras au top.";
  } else if (percent.value === 50) {
    return "⚖️ Tu es à pile 50%. On peut faire mieux !";
  } else if (percent.value >= 25) {
    return "🤔 Il y a encore du boulot… mais on ne lâche rien !";
  } else if (percent.value >= 1) {
    return "😅 C'était chaud… On révise un peu et on recommence ?";
  } else {
    return "💥 0% ?! Essaie encore… avec les yeux ouverts cette fois 😄";
  }
});

const feedbackClass = computed(() => {
  if (percent.value === 100) {
    return "text-success fw-bold"; // Vert et en gras
  } else if (percent.value >= 75) {
    return "text-primary fw-semibold"; // Bleu
  } else if (percent.value >= 51) {
    return "text-info"; // Turquoise
  } else if (percent.value === 50) {
    return "text-warning"; // Jaune
  } else if (percent.value >= 25) {
    return "text-orange"; // Couleur personnalisée (à ajouter)
  } else if (percent.value >= 1) {
    return "text-danger"; // Rouge
  } else {
    return "text-muted fst-italic"; // Gris clair et italique
  }
});

const resultImage = computed(() => {
  if (percent.value === 100) return '/img/Niv6.jpg';
  if (percent.value >= 75) return '/img/Niv5.jpg';
  if (percent.value >= 51) return '/img/Niv4.jpg';
  if (percent.value === 50) return '/img/Niv3.jpg';
  if (percent.value >= 25) return '/img/Niv2.jpg';
  if (percent.value >= 1) return '/img/Niv1.jpg';
  return '/img/Niv0.jpg';
});

function getColoredQuestion(question) {
  const match = question.match(/(\d+)\s*(.)\s*(\d+)/)
  if (!match) return question

  const [_, a, op, b] = match
  const colorA = colors[Math.floor(Math.random() * colors.length)]
  const colorB = colors[Math.floor(Math.random() * colors.length)]
  return `<span style="color:${colorA}">${a}</span> ${op} <span style="color:${colorB}">${b}</span>`
}

const renderedQuestion = ref('')
watch(currentQuestion, () => {
  animate.value = false
  setTimeout(() => {
    renderedQuestion.value = getColoredQuestion(currentQuestion.value.question)
    animate.value = true
    nextTick(() => {
      answerInput.value?.focus()
    })
  }, 50)
})

function startGame() {
  if (selectedOps.value.length === 0) {
    alert("Choisis au moins une opération.")
    return
  }

  const count = mode.value === 'fixed' ? questionCount.value : 100
  const url = buildMathUrl(selectedOps.value, count, digitRange.value)


  fetch(url)
    .then(res => res.json())
    .then(data => {
      exercises.value = data.exercises
      answers.value = []
      currentIndex.value = 0
      started.value = true
      gameOver.value = false
      currentAnswer.value = null
      renderedQuestion.value = getColoredQuestion(data.exercises[0].question)

      if (mode.value === 'timed') {
        timeLeft.value = duration.value
        timer = setInterval(() => {
          timeLeft.value--
          if (timeLeft.value <= 0) {
            clearInterval(timer)
            finishGame()
          }
        }, 1000)
      }
    })
}

function validateAnswer() {
  if (currentAnswer.value === null) return

  answers.value.push(currentAnswer.value)
  currentAnswer.value = null

  const isLastQuestion = currentIndex.value >= exercises.value.length - 1

  if (isLastQuestion || (mode.value === 'timed' && timeLeft.value <= 0)) {
    finishGame()
  } else {
    currentIndex.value++
    renderedQuestion.value = ''
    setTimeout(() => {
      renderedQuestion.value = getColoredQuestion(exercises.value[currentIndex.value].question)
    }, 100)
  }
}

function finishGame() {
  clearInterval(timer)
  renderedQuestion.value = ''
  gameOver.value = true
}

function resetGame() {
  exercises.value = []
  answers.value = []
  currentAnswer.value = null
  currentIndex.value = 0
  timeLeft.value = 0
  started.value = false
  gameOver.value = false
}
</script>

<style scoped>
.game-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 2rem;
}

.start-form {
  max-width: 600px;
  width: 100%;
}

.game-play {
  width: 100%;
}

.display-3 {
  font-size: 10vw;
}

.input-big {
  font-size: 10vw;
  width: 50%;
  margin: auto;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.text-orange {
  color: #fd7e14; /* Orange Bootstrap */
}

.result-img {
  max-width: 250px;
  height: auto;
}

</style>
