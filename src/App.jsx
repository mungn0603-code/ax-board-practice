import { useEffect, useState } from 'react'

const STORAGE_KEY = 'ax-board-ideas'

function loadIdeas() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    return saved ? JSON.parse(saved) : []
  } catch {
    return []
  }
}

export default function App() {
  const [ideas, setIdeas] = useState(loadIdeas)
  const [title, setTitle] = useState('')
  const [task, setTask] = useState('')
  const [idea, setIdea] = useState('')
  const [tag, setTag] = useState('')
  const [filter, setFilter] = useState('전체')
  const [message, setMessage] = useState('')

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(ideas))
  }, [ideas])

  const tags = ['전체', ...new Set(ideas.map((item) => item.tag).filter(Boolean))]
  const visible = filter === '전체' ? ideas : ideas.filter((item) => item.tag === filter)

  function addIdea(event) {
    event.preventDefault()
    if (!title.trim() || !task.trim() || !idea.trim()) {
      setMessage('제목, 대상 업무, AI 아이디어를 모두 입력해 주세요.')
      return
    }
    setIdeas((current) => [
      { id: Date.now(), title: title.trim(), task: task.trim(), idea: idea.trim(), tag: tag.trim() },
      ...current,
    ])
    setTitle('')
    setTask('')
    setIdea('')
    setTag('')
    setMessage('카드를 추가했습니다.')
  }

  function deleteIdea(id) {
    if (!window.confirm('이 카드를 삭제할까요?')) {
      setMessage('삭제를 취소했습니다.')
      return
    }
    setIdeas((current) => current.filter((item) => item.id !== id))
    setMessage('카드를 삭제했습니다.')
  }

  return (
    <main className="board">
      <h1>
        AX 보드 A <span className="count">아이디어 {ideas.length}개</span>
      </h1>

      <form className="card-form" onSubmit={addIdea}>
        <input aria-label="제목" placeholder="예: 설비 점검 기록 요약" value={title} onChange={(e) => setTitle(e.target.value)} />
        <input aria-label="대상 업무" placeholder="대상 업무" value={task} onChange={(e) => setTask(e.target.value)} />
        <textarea aria-label="AI 아이디어" placeholder="AI 활용 아이디어" value={idea} onChange={(e) => setIdea(e.target.value)} />
        <input aria-label="태그" placeholder="태그 (예: 생산, 품질)" value={tag} onChange={(e) => setTag(e.target.value)} />
        <button type="submit">카드 추가</button>
      </form>

      {message && <p className="message" role="status">{message}</p>}

      <label className="filter">
        태그 필터{' '}
        <select aria-label="태그 필터" value={filter} onChange={(e) => setFilter(e.target.value)}>
          {tags.map((name) => (
            <option key={name} value={name}>{name}</option>
          ))}
        </select>
      </label>

      {ideas.length === 0 && <p className="empty">아직 아이디어가 없어요</p>}

      <ul className="card-list">
        {visible.map((item) => (
          <li key={item.id} className="card">
            <h2>
              {item.title} {item.tag && <span className="tag">#{item.tag}</span>}
            </h2>
            <p className="task">대상 업무: {item.task}</p>
            <p>{item.idea}</p>
            <button type="button" onClick={() => deleteIdea(item.id)}>삭제</button>
          </li>
        ))}
      </ul>
    </main>
  )
}
