const people = {
  me: { name: 'Jordan Lee', email: 'jordan.lee@contoso.com', initials: 'JL' },
  nominee: { name: 'Priya Nair', email: 'priya.nair@contoso.com', initials: 'PN' },
  lead: { name: 'Marcus Chen', email: 'marcus.chen@contoso.com', initials: 'MC' },
}

const categories = {
  individual: [
    {
      id: 'innovation',
      title: 'Innovation Champion',
      description: 'Recognizes creative ideas that deliver meaningful improvements.',
      icon: 'spark',
      criteria: [
        ['Originality of the idea', 'Explain what made the idea distinctive and how it addressed an unmet need.'],
        ['Implementation and ownership', 'Describe how the nominee took the idea from concept to practical delivery.'],
        ['Measurable impact', 'Share the outcomes, improvements, or value that resulted from the idea.'],
      ],
    },
    {
      id: 'customer',
      title: 'Customer Impact',
      description: 'Recognizes exceptional service and measurable customer outcomes.',
      icon: 'heart',
      criteria: [
        ['Understanding customer needs', 'Show how the nominee identified and understood the customer’s priorities.'],
        ['Quality of service or solution', 'Describe the exceptional quality of the service or solution provided.'],
        ['Measurable customer outcomes', 'Share specific results, feedback, or improvements for the customer.'],
        ['Sustained customer commitment', 'Explain how the nominee maintained a lasting focus on customer success.'],
      ],
    },
    {
      id: 'execution',
      title: 'Excellence in Execution',
      description: 'Recognizes consistently outstanding delivery and ownership.',
      icon: 'target',
      criteria: [
        ['Quality and reliability', 'Describe how the nominee consistently delivered high-quality, dependable work.'],
        ['Ownership and accountability', 'Show how the nominee took responsibility and followed through on commitments.'],
        ['Results delivered', 'Share the outcomes achieved and why they mattered to the organization.'],
      ],
    },
  ],
  team: [
    {
      id: 'collaboration',
      title: 'Collaboration Excellence',
      description: 'Recognizes teams that succeed through strong cross-functional partnership.',
      icon: 'people',
      criteria: [
        ['Cross-functional collaboration', 'Describe how the team partnered effectively across functions or boundaries.'],
        ['Inclusive participation and knowledge sharing', 'Show how the team welcomed diverse perspectives and shared expertise.'],
        ['Collective outcomes', 'Share the results the team achieved by working together.'],
      ],
    },
    {
      id: 'business',
      title: 'Business Impact',
      description: 'Recognizes teams that deliver measurable organizational value.',
      icon: 'chart',
      criteria: [
        ['Alignment with business priorities', 'Explain how the team’s work supported strategic organizational priorities.'],
        ['Measurable results', 'Share specific business outcomes and the evidence used to measure them.'],
        ['Effective use of resources', 'Describe how the team used time, budget, and expertise responsibly.'],
        ['Sustainability of impact', 'Explain how the team’s results will continue to create value over time.'],
      ],
    },
    {
      id: 'transformation',
      title: 'Transformation & Innovation',
      description: 'Recognizes teams that introduce and sustain meaningful change.',
      icon: 'refresh',
      criteria: [
        ['Novel approach', 'Describe the new approach and what made it different from previous practice.'],
        ['Adoption and change management', 'Explain how the team helped people adopt and sustain the change.'],
        ['Measurable improvement', 'Share the improvements achieved and how they were measured.'],
        ['Scalability and sustainability', 'Show how the solution can grow and remain effective over time.'],
      ],
    },
  ],
}

const sampleResponses = [
  'Priya identified that our onboarding process created unnecessary handoffs for new enterprise customers. She designed a single intake workflow, brought Sales and Support into the discovery process, and tested the approach with three account teams. The result reduced average setup time from nine days to five while giving customers a clearer view of progress.',
  'Priya volunteered to lead the pilot from discovery through rollout. She built the implementation plan, facilitated weekly working sessions, and created a practical playbook so that account teams could adopt the new process consistently. When early feedback highlighted a reporting gap, she coordinated a solution within the same sprint.',
]

const nominations = [
  { ref: 'NOM-2026-00128', name: 'Priya Nair', type: 'Individual Award', category: 'Innovation Champion', date: 'Mar 12, 2026', status: 'Submitted' },
  { ref: 'DRAFT-00417', name: 'Digital Customer Experience Team', type: 'Team Award', category: 'Collaboration Excellence', date: 'Mar 10, 2026', status: 'Draft' },
  { ref: 'NOM-2026-00094', name: 'Elena Vasquez', type: 'Individual Award', category: 'Customer Impact', date: 'Feb 28, 2026', status: 'Submitted' },
  { ref: 'DRAFT-00381', name: 'Finance Modernization Team', type: 'Team Award', category: 'Not selected', date: 'Feb 24, 2026', status: 'Draft' },
]

const state = {
  view: 'new',
  step: 1,
  type: 'individual',
  categoryId: 'innovation',
  role: 'Senior Product Manager',
  level: 'L4',
  teamName: 'Digital Customer Experience Team',
  responses: {
    'innovation-0': {
      text: sampleResponses[0],
      files: [{ id: 1, name: 'Onboarding-results-summary.pdf', size: '1.2 MB', status: 'done', progress: 100 }],
      links: ['https://contoso.sharepoint.com/customer-onboarding-case-study'],
    },
    'innovation-1': { text: sampleResponses[1], files: [], links: [] },
  },
  errors: {},
  saveState: 'idle',
  confirm: false,
  submitState: 'idle',
  pendingChange: null,
  search: '',
  statusFilter: 'All statuses',
  typeFilter: 'All types',
}

const iconPaths = {
  award: '<path d="M12 15a6 6 0 1 0 0-12 6 6 0 0 0 0 12Z"/><path d="m8.5 14.5-1 6 4.5-2.5 4.5 2.5-1-6"/>',
  help: '<circle cx="12" cy="12" r="9"/><path d="M9.7 9a2.4 2.4 0 0 1 4.6 1c0 1.8-2.3 2-2.3 3.7"/><path d="M12 17h.01"/>',
  person: '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c.5-4 3-6 7-6s6.5 2 7 6"/>',
  people: '<circle cx="9" cy="8" r="3"/><path d="M3 19c.4-3.7 2.4-5.5 6-5.5s5.6 1.8 6 5.5"/><path d="M16 5.5a3 3 0 0 1 0 5.8M17 14c2.3.5 3.7 2.2 4 5"/>',
  chevron: '<path d="m9 18 6-6-6-6"/>',
  back: '<path d="m15 18-6-6 6-6"/>',
  check: '<path d="m5 12 4 4L19 6"/>',
  spark: '<path d="m12 3 1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5L12 3Z"/><path d="m18 15 .7 2.3L21 18l-2.3.7L18 21l-.7-2.3L15 18l2.3-.7L18 15Z"/>',
  heart: '<path d="M20.8 5.8c-2.1-2.2-5.6-2.2-7.8 0L12 7l-1.1-1.2a5.4 5.4 0 0 0-7.7 7.6L12 22l8.8-8.6a5.4 5.4 0 0 0 0-7.6Z"/>',
  target: '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4"/><path d="M12 12 20 4"/>',
  chart: '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
  refresh: '<path d="M20 7v5h-5"/><path d="M4 17v-5h5"/><path d="M6.1 8A7 7 0 0 1 18.7 7M17.9 16A7 7 0 0 1 5.3 17"/>',
  attach: '<path d="m20.5 11.5-8.9 8.9a6 6 0 0 1-8.5-8.5l9.6-9.6a4 4 0 0 1 5.7 5.7l-9.6 9.6a2 2 0 0 1-2.8-2.8l8.9-8.9"/>',
  link: '<path d="M10 13a5 5 0 0 0 7.5.5l2-2a5 5 0 0 0-7-7l-1.2 1.2"/><path d="M14 11a5 5 0 0 0-7.5-.5l-2 2a5 5 0 0 0 7 7l1.2-1.2"/>',
  file: '<path d="M6 2h8l4 4v16H6Z"/><path d="M14 2v5h5"/>',
  search: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
  save: '<path d="M4 3h13l3 3v15H4Z"/><path d="M8 3v6h8V3M8 21v-7h8v7"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7h.01"/>',
}

function icon(name, size = 20) {
  return `<svg aria-hidden="true" viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${iconPaths[name] || ''}</svg>`
}

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;')
}

function currentCategory() {
  return categories[state.type].find((item) => item.id === state.categoryId) || categories[state.type][0]
}

function nomineeName() {
  return state.type === 'individual' ? people.nominee.name : state.teamName
}

function hasResponses() {
  return Object.values(state.responses).some((response) => response.text || response.files.length || response.links.length)
}

function button(label, action, variant = 'primary', iconName = '', disabled = false) {
  return `<button class="btn btn-${variant}" data-action="${action}" ${disabled ? 'disabled' : ''}>${iconName ? icon(iconName, 17) : ''}<span>${label}</span></button>`
}

function header() {
  return `
    <header class="topbar">
      <button class="brand" data-action="home">
        <span class="logo-mark">${icon('award', 23)}</span>
        <span><strong>Contoso</strong><span class="brand-divider"></span><b>Employee &amp; Team Recognition Awards</b></span>
      </button>
      <div class="header-actions">
        <button class="header-link">${icon('help', 19)}<span>Help</span></button>
        <span class="header-rule"></span>
        <button class="user-menu"><span class="avatar">JL</span><span class="user-copy"><strong>Jordan Lee</strong><small>Signed in</small></span><span class="down">⌄</span></button>
      </div>
    </header>
    <nav class="main-nav">
      <div class="nav-inner">
        <button class="${state.view === 'new' ? 'active' : ''}" data-action="nav-new">${icon('award', 18)}New nomination</button>
        <button class="${state.view === 'mine' ? 'active' : ''}" data-action="nav-mine">${icon('file', 18)}My nominations</button>
      </div>
    </nav>`
}

function stepper() {
  const labels = ['Nominee details', 'Award category', 'Criteria & evidence', 'Review & submit']
  return `<div class="stepper-wrap"><div class="stepper" aria-label="Nomination progress">${labels.map((label, index) => {
    const number = index + 1
    const status = number < state.step ? 'complete' : number === state.step ? 'current' : 'upcoming'
    return `<button class="step ${status}" data-action="step" data-step="${number}" ${number > state.step ? 'disabled' : ''}>
      <span class="step-marker">${number < state.step ? icon('check', 15) : number}</span>
      <span class="step-text"><small>Step ${number}</small><strong>${label}</strong></span>
      ${index < labels.length - 1 ? '<span class="step-line"></span>' : ''}
    </button>`
  }).join('')}</div></div>`
}

function pageIntro(title, subtitle, eyebrow = '') {
  return `<div class="page-intro">${eyebrow ? `<span class="eyebrow">${eyebrow}</span>` : ''}<h1>${title}</h1><p>${subtitle}</p></div>`
}

function personPicker(label, person, required = true) {
  return `<div class="field"><label>${label}${required ? '<span class="required"> *</span>' : ''}</label>
    <div class="person-picker" tabindex="0">${icon('search', 18)}<span class="avatar avatar-sm">${person.initials}</span>
      <span class="person-copy"><strong>${person.name}</strong><small>${person.email}</small></span><span class="picker-action">Change</span>
    </div></div>`
}

function textField(label, id, value, required = true, placeholder = '') {
  const error = state.errors[id]
  return `<div class="field ${error ? 'has-error' : ''}"><label for="${id}">${label}${required ? '<span class="required"> *</span>' : ''}</label>
    <input id="${id}" data-field="${id}" value="${escapeHtml(value)}" placeholder="${escapeHtml(placeholder)}">
    ${error ? `<div class="field-error">${icon('info', 15)}${error}</div>` : ''}</div>`
}

function levelField() {
  return `<div class="field"><label for="level">Employee level<span class="required"> *</span></label>
    <select id="level" data-field="level"><option value="">Select a level</option>${['L1', 'L2', 'L3', 'L4', 'L5', 'L6'].map((level) => `<option ${state.level === level ? 'selected' : ''}>${level}</option>`).join('')}</select>
    ${state.errors.level ? `<div class="field-error">${icon('info', 15)}${state.errors.level}</div>` : ''}</div>`
}

function actions(back, nextLabel = 'Continue', nextAction = 'continue') {
  return `<div class="form-actions"><div>${back ? button('Back', 'back', 'secondary', 'back') : ''}</div>
    <div>${button('Save draft', 'save', 'subtle', 'save')}${button(nextLabel, nextAction)}</div></div>`
}

function nomineeScreen() {
  return `<main class="page">${pageIntro('Recognize someone who makes a difference', 'Nominate a colleague or team and tell us about their impact.')}
    <div class="content-card form-card">
      <section><div class="section-heading"><div><span class="section-number">1</span><h2>Who is making the nomination?</h2></div><p>Your details are prefilled from your profile.</p></div>${personPicker('Nominated by', people.me)}</section>
      <div class="section-rule"></div>
      <section><div class="section-heading"><div><span class="section-number">2</span><h2>What type of nomination is this?</h2></div><p>Select one option. You can change this before submission.</p></div>
        <div class="type-grid">${typeChoice('individual', 'person', 'Individual Award', 'Recognize one colleague for their outstanding contribution.')}${typeChoice('team', 'people', 'Team Award', 'Celebrate a team that achieved exceptional results together.')}</div>
      </section>
      <div class="section-rule"></div>
      ${state.type === 'individual' ? individualFields() : teamFields()}
    </div>${actions(false)}</main>`
}

function typeChoice(type, iconName, title, copy) {
  const selected = state.type === type
  return `<button class="choice-card ${selected ? 'selected' : ''}" data-action="choose-type" data-type="${type}">
    <span class="choice-icon">${icon(iconName, 25)}</span><span class="choice-copy"><strong>${title}</strong><small>${copy}</small></span>
    <span class="radio">${selected ? '<span></span>' : ''}</span></button>`
}

function individualFields() {
  return `<section class="dynamic-section"><div class="section-heading"><div><span class="section-number">3</span><h2>Tell us about the nominee</h2></div><p>Search by name or email to find a colleague.</p></div>
    ${personPicker('Nominated person', people.nominee)}
    <div class="two-col">${textField('Employee role', 'role', state.role, true, 'e.g., Senior Product Manager')}${levelField()}</div>
  </section>`
}

function teamFields() {
  return `<section class="dynamic-section"><div class="section-heading"><div><span class="section-number">3</span><h2>Tell us about the team</h2></div><p>Provide the team’s name and primary contact.</p></div>
    ${textField('Nominated team name', 'teamName', state.teamName, true, 'Enter the official team name')}
    ${personPicker('Team lead / primary contact', people.lead)}
    <div class="two-col">${textField('Primary contact role', 'role', state.role)}${levelField()}</div>
    <div class="field"><label>Optional team members</label><div class="multi-picker" tabindex="0"><span class="person-chip"><span class="avatar avatar-xs">AK</span>Aisha Khan <b>×</b></span><span class="person-chip"><span class="avatar avatar-xs">DR</span>Diego Ruiz <b>×</b></span><span class="search-prompt">Search for people…</span></div></div>
    <div class="info-banner">${icon('info', 19)}<span>Role and level refer to the team’s primary contact, not the entire team.</span></div>
  </section>`
}

function summaryStrip(showCategory = false) {
  const category = currentCategory()
  return `<div class="summary-strip"><div><span class="avatar summary-avatar">${state.type === 'individual' ? 'PN' : 'DX'}</span><span><small>${state.type === 'individual' ? 'Individual nominee' : 'Nominated team'}</small><strong>${escapeHtml(nomineeName())}</strong></span></div>
    <div><small>Nomination type</small><strong>${state.type === 'individual' ? 'Individual Award' : 'Team Award'}</strong></div>
    ${showCategory ? `<div><small>Award category</small><strong>${category.title}</strong></div>` : ''}</div>`
}

function categoryScreen() {
  return `<main class="page">${pageIntro('Choose an award category', 'Select the category that best reflects the nominee’s contribution.', 'Step 2 of 4')}
    ${summaryStrip()}<div class="category-grid">${categories[state.type].map((category) => {
      const selected = category.id === state.categoryId
      return `<button class="category-card ${selected ? 'selected' : ''}" data-action="choose-category" data-category="${category.id}">
        <span class="category-top"><span class="category-icon">${icon(category.icon, 25)}</span><span class="radio">${selected ? '<span></span>' : ''}</span></span>
        <strong>${category.title}</strong><p>${category.description}</p><span class="criteria-count">${icon('file', 16)}${category.criteria.length} criteria</span>
      </button>`
    }).join('')}</div>
    ${state.errors.category ? `<div class="page-error">${icon('info', 17)}${state.errors.category}</div>` : ''}
    <div class="selection-note">${icon('info', 19)}<span>You can select one award category per nomination. Criteria will load automatically in the next step.</span></div>${actions(true)}</main>`
}

function progressSummary() {
  const category = currentCategory()
  const complete = category.criteria.filter((_, index) => state.responses[`${category.id}-${index}`]?.text.trim()).length
  return `<aside class="progress-card"><div class="progress-title"><div><span>Response progress</span><strong>${complete} of ${category.criteria.length}</strong></div><div class="progress-bar"><span style="width:${complete / category.criteria.length * 100}%"></span></div></div>
    <div class="progress-list">${category.criteria.map((criterion, index) => {
      const done = Boolean(state.responses[`${category.id}-${index}`]?.text.trim())
      return `<a href="#criterion-${index}" class="${done ? 'done' : ''}"><span>${done ? icon('check', 14) : index + 1}</span><small>${criterion[0]}</small></a>`
    }).join('')}</div><div class="autosave">${icon('save', 16)}Responses are saved when you select “Save draft”.</div></aside>`
}

function criterionCard(criterion, index) {
  const category = currentCategory()
  const key = `${category.id}-${index}`
  const response = state.responses[key] || { text: '', files: [], links: [] }
  return `<article class="criterion-card" id="criterion-${index}">
    <div class="criterion-header"><span class="criterion-number">${index + 1}</span><div><h2>${criterion[0]}</h2><p>${criterion[1]}</p></div>${response.text.trim() ? `<span class="complete-badge">${icon('check', 14)}Complete</span>` : ''}</div>
    <div class="response-area"><label for="response-${index}">Describe how the nominee meets this criterion <span class="required">*</span></label>
      <textarea id="response-${index}" data-response="${key}" maxlength="2000" placeholder="Describe the situation, actions taken, and results achieved.">${escapeHtml(response.text)}</textarea>
      <div class="textarea-meta"><span>Include specific examples and measurable outcomes where possible.</span><span>${response.text.length.toLocaleString()} / 2,000</span></div>
    </div>
    <div class="evidence-area"><div class="evidence-heading"><div>${icon('attach', 18)}<strong>Supporting evidence <span>Optional</span></strong></div><p>Add documents, screenshots, or links that support this response.</p></div>
      ${response.files.map((file) => evidenceFile(key, file)).join('')}
      ${response.links.map((link, linkIndex) => evidenceLink(key, link, linkIndex)).join('')}
      <div class="evidence-controls"><input class="file-input" type="file" id="file-${index}" data-file="${key}">
        ${button('Add attachment', `file-picker:${index}`, 'secondary', 'attach')}
        <div class="link-control">${icon('link', 17)}<input data-link-input="${key}" placeholder="Paste an evidence link"><button data-action="add-link" data-key="${key}">Add link</button></div>
      </div>
    </div></article>`
}

function evidenceFile(key, file) {
  return `<div class="evidence-row ${file.status}"><span class="file-icon">${icon('file', 19)}</span>
    <span class="evidence-copy"><strong>${escapeHtml(file.name)}</strong><small>${file.status === 'uploading' ? `Uploading… ${file.progress}%` : file.status === 'error' ? 'Upload failed — file must be under 5 MB' : file.size}</small>
    ${file.status === 'uploading' ? `<span class="upload-track"><i style="width:${file.progress}%"></i></span>` : ''}</span>
    ${file.status === 'error' ? `<button data-action="retry-file" data-key="${key}" data-id="${file.id}">Retry</button>` : ''}
    <button class="remove" data-action="remove-file" data-key="${key}" data-id="${file.id}">Remove</button></div>`
}

function evidenceLink(key, link, index) {
  return `<div class="evidence-row"><span class="file-icon link">${icon('link', 19)}</span><span class="evidence-copy"><strong>Customer onboarding case study</strong><small>${escapeHtml(link)}</small></span><button class="remove" data-action="remove-link" data-key="${key}" data-index="${index}">Remove</button></div>`
}

function criteriaScreen() {
  const category = currentCategory()
  return `<main class="page page-wide">${pageIntro('Tell us about their impact', 'Respond to each criterion and add supporting evidence where it helps tell the story.', 'Step 3 of 4')}
    ${summaryStrip(true)}<div class="criteria-layout"><div class="criteria-main">${progressSummary()}
      ${state.errors.criteria ? `<div class="page-error">${icon('info', 17)}${state.errors.criteria}</div>` : ''}
      ${category.criteria.map(criterionCard).join('')}</div>${progressSummary()}</div>${actions(true, 'Review nomination')}</main>`
}

function reviewScreen() {
  const category = currentCategory()
  return `<main class="page review-page">${pageIntro('Review your nomination', 'Check the details below. You can edit any section before submitting.', 'Step 4 of 4')}
    <div class="review-card">
      ${reviewSection('Nominee details', 1, `<div class="review-grid"><div><small>Nominated by</small><strong>Jordan Lee</strong><span>jordan.lee@contoso.com</span></div><div><small>Nomination type</small><strong>${state.type === 'individual' ? 'Individual Award' : 'Team Award'}</strong></div><div><small>${state.type === 'individual' ? 'Nominated person' : 'Nominated team'}</small><strong>${escapeHtml(nomineeName())}</strong>${state.type === 'individual' ? '<span>priya.nair@contoso.com</span>' : ''}</div><div><small>${state.type === 'individual' ? 'Employee role & level' : 'Primary contact'}</small><strong>${escapeHtml(state.role)}</strong><span>${state.level}</span></div></div>`)}
      ${reviewSection('Award category', 2, `<div class="review-category"><span class="category-icon">${icon(category.icon, 23)}</span><div><strong>${category.title}</strong><p>${category.description}</p></div></div>`)}
      ${reviewSection('Criteria & evidence', 3, `<div class="review-responses">${category.criteria.map((criterion, index) => reviewResponse(category, criterion, index)).join('')}</div>`)}
    </div>
    <div class="confirmation-box ${state.errors.confirm ? 'has-error' : ''}"><label><input id="confirm" type="checkbox" ${state.confirm ? 'checked' : ''}><span class="custom-check">${state.confirm ? icon('check', 15) : ''}</span><span>I confirm that this nomination is accurate to the best of my knowledge. <b>*</b></span></label>${state.errors.confirm ? `<div class="field-error">${icon('info', 15)}${state.errors.confirm}</div>` : ''}</div>
    ${state.submitState === 'error' ? `<div class="page-error">${icon('info', 17)}We couldn’t submit this nomination. Check your connection and try again.</div>` : ''}
    ${actions(true, state.submitState === 'submitting' ? 'Submitting…' : 'Submit nomination', 'submit')}</main>`
}

function reviewSection(title, step, content) {
  return `<section class="review-section"><div class="review-section-head"><h2>${title}</h2><button data-action="edit" data-step="${step}">Edit</button></div>${content}</section>`
}

function reviewResponse(category, criterion, index) {
  const response = state.responses[`${category.id}-${index}`] || { text: '', files: [], links: [] }
  return `<div class="review-response"><span class="criterion-number">${index + 1}</span><div><h3>${criterion[0]}</h3><p>${escapeHtml(response.text || 'No response provided.')}</p>
    ${response.files.length || response.links.length ? `<div class="review-evidence">${response.files.map((file) => `<span>${icon('file', 15)}${escapeHtml(file.name)}</span>`).join('')}${response.links.map(() => `<span>${icon('link', 15)}Evidence link</span>`).join('')}</div>` : ''}</div></div>`
}

function confirmationScreen() {
  const category = currentCategory()
  return `<main class="confirmation-page"><div class="success-mark">${icon('check', 42)}</div><span class="success-eyebrow">Submission complete</span>
    <h1>Nomination submitted</h1><p>Thank you for recognizing the people who make a difference at Contoso.</p>
    <div class="reference-card"><small>Reference number</small><strong>NOM-2026-00128</strong><div class="reference-details">
      <span><small>Nominee</small><b>${escapeHtml(nomineeName())}</b></span><span><small>Award category</small><b>${category.title}</b></span>
      <span><small>Submission date</small><b>March 12, 2026</b></span><span><small>Status</small><b class="status submitted"><i></i>Submitted</b></span>
    </div></div><div class="success-note">${icon('info', 19)}<span>A confirmation has been sent to <strong>jordan.lee@contoso.com</strong>. Keep the reference number for your records.</span></div>
    <div class="success-actions">${button('View nomination', 'view-submission', 'secondary')}${button('Create another nomination', 'reset')}</div><button class="text-link" data-action="nav-mine">Go to My nominations</button></main>`
}

function myNominations() {
  const filtered = nominations.filter((item) =>
    (state.statusFilter === 'All statuses' || item.status === state.statusFilter) &&
    (state.typeFilter === 'All types' || item.type.startsWith(state.typeFilter)) &&
    (item.name.toLowerCase().includes(state.search.toLowerCase()) || item.ref.toLowerCase().includes(state.search.toLowerCase()))
  )
  return `<main class="page my-page"><div class="list-heading">${pageIntro('My nominations', 'Continue a draft or review nominations you’ve submitted.')}${button('New nomination', 'reset', 'primary', 'award')}</div>
    <div class="list-card"><div class="filters"><div class="search-box">${icon('search', 18)}<input id="search" value="${escapeHtml(state.search)}" placeholder="Search by nominee or reference"></div>
      <select id="type-filter"><option>All types</option><option ${state.typeFilter === 'Individual' ? 'selected' : ''}>Individual</option><option ${state.typeFilter === 'Team' ? 'selected' : ''}>Team</option></select>
      <select id="status-filter"><option>All statuses</option><option ${state.statusFilter === 'Draft' ? 'selected' : ''}>Draft</option><option ${state.statusFilter === 'Submitted' ? 'selected' : ''}>Submitted</option></select></div>
      ${filtered.length ? nominationTable(filtered) : `<div class="empty-state"><span>${icon('search', 28)}</span><h2>No nominations found</h2><p>Try changing your search or filters to see more results.</p>${button('Clear filters', 'clear-filters', 'secondary')}</div>`}
      <div class="table-footer">Showing ${filtered.length} of ${nominations.length} nominations</div>
    </div><div class="prototype-note">${icon('info', 18)}This is a design prototype. Employee lookup, file storage, draft persistence, and submission services are simulated.</div></main>`
}

function nominationTable(items) {
  return `<div class="table-wrap"><table><thead><tr><th>Reference</th><th>Nominee / team</th><th>Nomination type</th><th>Award category</th><th>Last updated</th><th>Status</th><th>Action</th></tr></thead>
    <tbody>${items.map((item) => `<tr><td data-label="Reference"><b>${item.ref}</b></td><td data-label="Nominee / team"><strong>${item.name}</strong></td><td data-label="Nomination type">${item.type}</td><td data-label="Award category">${item.category}</td><td data-label="Last updated">${item.date}</td><td data-label="Status"><span class="status ${item.status.toLowerCase()}"><i></i>${item.status}</span></td><td><button class="row-action" data-action="open-nomination" data-draft="${item.status === 'Draft'}">${item.status === 'Draft' ? 'Continue editing' : 'View'}${icon('chevron', 15)}</button></td></tr>`).join('')}</tbody></table></div>`
}

function toast() {
  if (state.saveState === 'idle') return ''
  const message = state.saveState === 'saving' ? 'Saving draft…' : state.saveState === 'success' ? 'Draft saved' : 'Draft couldn’t be saved'
  return `<div class="toast ${state.saveState}">${state.saveState === 'saving' ? '<span class="spinner"></span>' : icon(state.saveState === 'success' ? 'check' : 'info', 19)}
    <div><strong>${message}</strong>${state.saveState === 'success' ? '<small>Your changes were saved at 10:42 AM.</small>' : ''}</div>${state.saveState === 'error' ? '<button data-action="save">Retry</button>' : ''}</div>`
}

function modal() {
  if (!state.pendingChange) return ''
  return `<div class="modal-backdrop"><div class="modal" role="dialog" aria-modal="true" aria-labelledby="change-title"><div class="modal-icon">${icon('info', 24)}</div><div><h2 id="change-title">Change this selection?</h2><p>Changing the nomination type or award category will clear the current category, criterion responses, and supporting evidence.</p></div>
    <div class="modal-actions">${button('Cancel', 'cancel-change', 'secondary')}${button('Change and clear', 'confirm-change', 'danger')}</div></div></div>`
}

function render() {
  let screen
  if (state.view === 'mine') screen = myNominations()
  else if (state.step === 1) screen = nomineeScreen()
  else if (state.step === 2) screen = categoryScreen()
  else if (state.step === 3) screen = criteriaScreen()
  else if (state.step === 4) screen = reviewScreen()
  else screen = confirmationScreen()

  document.querySelector('#app').innerHTML = `<div class="app-shell">${header()}${state.view === 'new' && state.step < 5 ? stepper() : ''}${screen}${toast()}${modal()}</div>`
}

function requestClearChange(change) {
  if (hasResponses()) {
    state.pendingChange = change
    render()
  } else {
    applyClearChange(change)
  }
}

function applyClearChange(change) {
  if (change.kind === 'type') {
    state.type = change.value
    state.categoryId = categories[change.value][0].id
  } else {
    state.categoryId = change.value
  }
  state.responses = {}
  state.pendingChange = null
  render()
}

function saveDraft() {
  state.saveState = 'saving'
  render()
  window.setTimeout(() => {
    state.saveState = navigator.onLine ? 'success' : 'error'
    render()
  }, 700)
  window.setTimeout(() => {
    state.saveState = 'idle'
    render()
  }, 3500)
}

function validateAndContinue() {
  state.errors = {}
  if (state.step === 1) {
    if (!state.role.trim()) state.errors.role = 'Enter the employee’s role.'
    if (!state.level) state.errors.level = 'Select an employee level.'
    if (state.type === 'team' && !state.teamName.trim()) state.errors.teamName = 'Enter the nominated team name.'
  }
  if (state.step === 2 && !state.categoryId) state.errors.category = 'Choose one award category to continue.'
  if (state.step === 3) {
    const category = currentCategory()
    if (category.criteria.some((_, index) => !state.responses[`${category.id}-${index}`]?.text.trim())) {
      state.errors.criteria = 'Add a written response for every criterion before continuing.'
    }
  }
  if (Object.keys(state.errors).length) {
    render()
    return
  }
  state.step = Math.min(4, state.step + 1)
  window.scrollTo({ top: 0, behavior: 'smooth' })
  render()
}

function resetNomination() {
  Object.assign(state, {
    view: 'new',
    step: 1,
    type: 'individual',
    categoryId: 'innovation',
    responses: {},
    errors: {},
    confirm: false,
    submitState: 'idle',
  })
  render()
}

function submitNomination() {
  if (state.submitState === 'submitting') return
  if (!state.confirm) {
    state.errors = { confirm: 'Confirm the nomination before submitting.' }
    render()
    return
  }
  state.errors = {}
  state.submitState = 'submitting'
  render()
  window.setTimeout(() => {
    if (!navigator.onLine) {
      state.submitState = 'error'
    } else {
      state.submitState = 'idle'
      state.step = 5
      window.scrollTo(0, 0)
    }
    render()
  }, 1500)
}

function addFile(key, file) {
  if (!file) return
  const response = state.responses[key] || { text: '', files: [], links: [] }
  const id = Date.now()
  const upload = { id, name: file.name, size: `${(file.size / 1024 / 1024).toFixed(1)} MB`, status: 'uploading', progress: 15 }
  response.files.push(upload)
  state.responses[key] = response
  render()
  window.setTimeout(() => {
    const stored = state.responses[key]?.files.find((item) => item.id === id)
    if (!stored) return
    stored.status = file.size > 5 * 1024 * 1024 ? 'error' : 'done'
    stored.progress = stored.status === 'error' ? 72 : 100
    render()
  }, 950)
}

document.addEventListener('input', (event) => {
  const target = event.target
  if (target.matches('[data-field]')) {
    state[target.dataset.field] = target.value
  }
  if (target.matches('[data-response]')) {
    const key = target.dataset.response
    state.responses[key] ||= { text: '', files: [], links: [] }
    state.responses[key].text = target.value
    const counter = target.closest('.response-area').querySelector('.textarea-meta span:last-child')
    counter.textContent = `${target.value.length.toLocaleString()} / 2,000`
  }
  if (target.id === 'search') {
    state.search = target.value
    render()
    const search = document.querySelector('#search')
    search?.focus()
    search?.setSelectionRange(state.search.length, state.search.length)
  }
})

document.addEventListener('change', (event) => {
  const target = event.target
  if (target.matches('[data-field]')) state[target.dataset.field] = target.value
  if (target.id === 'confirm') {
    state.confirm = target.checked
    state.errors.confirm = ''
    render()
  }
  if (target.id === 'type-filter') {
    state.typeFilter = target.value
    render()
  }
  if (target.id === 'status-filter') {
    state.statusFilter = target.value
    render()
  }
  if (target.matches('[data-file]')) addFile(target.dataset.file, target.files?.[0])
})

document.addEventListener('click', (event) => {
  const trigger = event.target.closest('[data-action]')
  if (!trigger) return
  const action = trigger.dataset.action

  if (action === 'home' || action === 'nav-new') {
    state.view = 'new'
    render()
  } else if (action === 'nav-mine') {
    state.view = 'mine'
    render()
  } else if (action === 'step' || action === 'edit') {
    state.step = Number(trigger.dataset.step)
    render()
  } else if (action === 'choose-type' && trigger.dataset.type !== state.type) {
    requestClearChange({ kind: 'type', value: trigger.dataset.type })
  } else if (action === 'choose-category' && trigger.dataset.category !== state.categoryId) {
    requestClearChange({ kind: 'category', value: trigger.dataset.category })
  } else if (action === 'continue') {
    validateAndContinue()
  } else if (action === 'back') {
    state.step = Math.max(1, state.step - 1)
    render()
  } else if (action === 'save') {
    saveDraft()
  } else if (action === 'submit') {
    submitNomination()
  } else if (action === 'cancel-change') {
    state.pendingChange = null
    render()
  } else if (action === 'confirm-change') {
    applyClearChange(state.pendingChange)
  } else if (action.startsWith('file-picker:')) {
    document.querySelector(`#file-${action.split(':')[1]}`)?.click()
  } else if (action === 'add-link') {
    const key = trigger.dataset.key
    const input = document.querySelector(`[data-link-input="${key}"]`)
    if (input.value.trim()) {
      state.responses[key] ||= { text: '', files: [], links: [] }
      state.responses[key].links.push(input.value.trim())
      render()
    }
  } else if (action === 'remove-link') {
    state.responses[trigger.dataset.key].links.splice(Number(trigger.dataset.index), 1)
    render()
  } else if (action === 'remove-file') {
    const response = state.responses[trigger.dataset.key]
    response.files = response.files.filter((file) => file.id !== Number(trigger.dataset.id))
    render()
  } else if (action === 'retry-file') {
    const file = state.responses[trigger.dataset.key].files.find((item) => item.id === Number(trigger.dataset.id))
    file.status = 'done'
    file.progress = 100
    render()
  } else if (action === 'view-submission') {
    state.step = 4
    render()
  } else if (action === 'reset') {
    resetNomination()
  } else if (action === 'open-nomination') {
    state.view = 'new'
    state.step = trigger.dataset.draft === 'true' ? 2 : 4
    render()
  } else if (action === 'clear-filters') {
    state.search = ''
    state.typeFilter = 'All types'
    state.statusFilter = 'All statuses'
    render()
  }
})

render()
