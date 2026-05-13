import { useMemo, useState } from 'react';

type RiskConcern = 'medical' | 'critical_illness' | 'life' | 'accident' | 'retirement' | 'education' | 'wealth';

type CustomerProfile = {
  name?: string;
  age: number;
  family_role: string;
  annual_budget: number;
  existing_coverage: string;
  concerns: RiskConcern[];
  risk_preference: 'conservative' | 'balanced' | 'aggressive';
};

type ChatResponse = {
  answer: string;
  suggested_actions: string[];
  compliance_notes: string[];
};

const concernOptions: Array<{ value: RiskConcern; label: string }> = [
  { value: 'medical', label: '医疗' },
  { value: 'critical_illness', label: '重疾' },
  { value: 'life', label: '寿险责任' },
  { value: 'accident', label: '意外' },
  { value: 'retirement', label: '养老' },
  { value: 'education', label: '教育金' },
  { value: 'wealth', label: '财富规划' },
];

const initialCustomer: CustomerProfile = {
  name: '王先生',
  age: 35,
  family_role: '家庭经济支柱，有娃，有房贷',
  annual_budget: 8000,
  existing_coverage: '有社保，暂无商业保险',
  concerns: ['medical', 'critical_illness', 'life'],
  risk_preference: 'balanced',
};

async function postChat(message: string, customer: CustomerProfile): Promise<ChatResponse> {
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, customer }),
  });
  if (!res.ok) {
    throw new Error(`请求失败：${res.status}`);
  }
  return res.json();
}

export default function App() {
  const [customer, setCustomer] = useState<CustomerProfile>(initialCustomer);
  const [message, setMessage] = useState('客户说预算有限，想知道先买什么更合适');
  const [result, setResult] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const selectedConcerns = useMemo(() => new Set(customer.concerns), [customer.concerns]);

  const updateCustomer = <K extends keyof CustomerProfile>(key: K, value: CustomerProfile[K]) => {
    setCustomer((prev) => ({ ...prev, [key]: value }));
  };

  const toggleConcern = (concern: RiskConcern) => {
    const next = new Set(selectedConcerns);
    if (next.has(concern)) next.delete(concern);
    else next.add(concern);
    updateCustomer('concerns', Array.from(next));
  };

  const runAssistant = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await postChat(message, customer);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '未知错误');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Insurance Agent Assistant MVP</p>
          <h1>保险代理人助手</h1>
          <p>客户需求采集、保障缺口分析、产品推荐草案、异议处理话术和合规提醒。</p>
        </div>
        <button onClick={runAssistant} disabled={loading}>{loading ? '分析中…' : '生成建议'}</button>
      </section>

      <section className="grid">
        <div className="card form-card">
          <h2>客户画像</h2>
          <label>
            客户姓名
            <input value={customer.name ?? ''} onChange={(e) => updateCustomer('name', e.target.value)} />
          </label>
          <label>
            年龄
            <input type="number" value={customer.age} onChange={(e) => updateCustomer('age', Number(e.target.value))} />
          </label>
          <label>
            家庭角色
            <input value={customer.family_role} onChange={(e) => updateCustomer('family_role', e.target.value)} />
          </label>
          <label>
            年保费预算（元）
            <input type="number" value={customer.annual_budget} onChange={(e) => updateCustomer('annual_budget', Number(e.target.value))} />
          </label>
          <label>
            已有保障
            <textarea value={customer.existing_coverage} onChange={(e) => updateCustomer('existing_coverage', e.target.value)} />
          </label>
          <div>
            <span className="label-title">关注风险</span>
            <div className="chips">
              {concernOptions.map((option) => (
                <button
                  className={selectedConcerns.has(option.value) ? 'chip active' : 'chip'}
                  key={option.value}
                  onClick={() => toggleConcern(option.value)}
                  type="button"
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>
          <label>
            沟通问题
            <textarea value={message} onChange={(e) => setMessage(e.target.value)} />
          </label>
        </div>

        <div className="card result-card">
          <h2>助手输出</h2>
          {error && <div className="error">{error}</div>}
          {!result && !error && <p className="muted">点击“生成建议”查看 MVP 输出。</p>}
          {result && (
            <>
              <pre>{result.answer}</pre>
              <h3>下一步动作</h3>
              <ul>{result.suggested_actions.map((item) => <li key={item}>{item}</li>)}</ul>
              <h3>合规提醒</h3>
              <ul>{result.compliance_notes.map((item) => <li key={item}>{item}</li>)}</ul>
            </>
          )}
        </div>
      </section>
    </main>
  );
}
