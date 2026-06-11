const lessonButtons = document.getElementById('lessonButtons');
const lessonTitleElement = document.getElementById('lessonTitle');
const lessonOutput = document.getElementById('lessonOutput');
const lessonPlaceholder = document.getElementById('lessonPlaceholder');
let activeButton = null;
const viewHistory = [];

// Hard-coded lesson map (client-side) based on workspace structure.
const structure = {
  'OANH VŨ': {
    sections: {
      'MỞ MẮT': {
        sections: {
          'PHẬT PHÁP': {
            basePath: 'data/oanh_vũ/mở_mắt/phật pháp',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt'
            ]
          },
          'HOẠT ĐỘNG THANH NIÊN VÀ XÃ HỘI': {
            basePath: 'data/oanh_vũ/mở_mắt/hoạt_động_thanh_niên_và_xã_hội',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt','bài_13.txt','bài_14.txt'
            ]
          },
          'VĂN NGHỆ': {
            basePath: 'data/oanh_vũ/mở_mắt/văn_nghệ',
            files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt']
          }
        }
      },
      'CÁNH MỀM': {
        sections: {
          'PHẬT PHÁP': {
            introFile: 'data/oanh_vũ/cánh_mềm/phật pháp/giới_thiệu.txt',
            basePath: 'data/oanh_vũ/cánh_mềm/phật pháp',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt'
            ]
          },
          'HOẠT ĐỘNG THANH NIÊN VÀ XÃ HỘI': {
            introFile: 'data/oanh_vũ/cánh_mềm/hoạt_động_thanh_niên_và_xã_hội/giới_thiệu.txt',
            basePath: 'data/oanh_vũ/cánh_mềm/hoạt_động_thanh_niên_và_xã_hội',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt','bài_13.txt','bài_14.txt','bài_15.txt','bài_16.txt','bài_17.txt','bài_18.txt','bài_19.txt'
            ]
          },
          'VĂN NGHỆ': {
            introFile: 'data/oanh_vũ/cánh_mềm/văn_nghệ/giới_thiệu.txt',
            basePath: 'data/oanh_vũ/cánh_mềm/văn_nghệ',
            files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt']
          }
        }
      }
    }
  },
  'NGÀNH THIẾU': {
    sections: {
      'HƯỚNG THIỆN': {
        sections: {
          'PHẬT PHÁP': {
            basePath: 'data/ngành_thiếu/hướng_thiện/phật_pháp',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt','bài_13.txt','bài_14.txt'
            ]
          },
          'HOẠT ĐỘNG THANH NIÊN': {
            sections: {
              'CỨU THƯƠNG': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/cứu_thương/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/cứu_thương', files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt'] },
              'DẤU ĐI ĐƯỜNG': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/dấu_đi_đường/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/dấu_đi_đường', files: ['bài_1.txt','bài_2.txt'] },
              'DỰNG LỀU': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/dựng_lều/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/dựng_lều', files: ['bài_1.txt','bài_2.txt'] },
              'GÚT DÂY': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/gút_dây/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/gút_dây', files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt'] },
              'PHƯƠNG HƯỚNG': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/phương_hướng/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/phương_hướng', files: ['bài_1.txt','bài_2.txt'] },
              'MẬT THƯ': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/mật_thư/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/mật_thư', files: ['bài_1.txt','bài_2.txt'] },
              'THƯỜNG THỨC': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/thường_thức/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/thường_thức', files: ['bài_1.txt'] },
              'TRUYỀN TIN': { introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/truyền_tin/giới_thiệu.txt', basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_thanh_niên/truyền_tin', files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt'] }
            }
          },
          'HOẠT ĐỘNG XÃ HỘI': {
            introFile: 'data/ngành_thiếu/hướng_thiện/hoạt_động_xã_hội/giới_thiệu.txt',
            basePath: 'data/ngành_thiếu/hướng_thiện/hoạt_động_xã_hội',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt'
            ]
          },
          'VĂN NGHỆ': {
            introFile: 'data/ngành_thiếu/hướng_thiện/văn_nghệ/giới_thiệu.txt',
            basePath: 'data/ngành_thiếu/hướng_thiện/văn_nghệ',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','danh_sách_bài_hát.txt'
            ]
          }
        }
      },
      'SƠ THIỆN': {
        sections: {
          'PHẬT PHÁP': {
            basePath: 'data/ngành_thiếu/sơ_thiện/phật_pháp',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt','bài_8.txt','bài_9.txt','bài_10.txt','bài_11.txt','bài_12.txt','bài_13.txt','bài_14.txt'
            ]
          },
          'HOẠT ĐỘNG THANH NIÊN': {
            sections: {
              'CỨU THƯƠNG': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/cứu_thương/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/cứu_thương', files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt'] },
              'DẤU ĐI ĐƯỜNG': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/dấu_đi_đường/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/dấu_đi_đường', files: ['bài_1.txt','bài_2.txt'] },
              'DỰNG LỀU': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/dựng_lều/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/dựng_lều', files: ['bài_1.txt','bài_2.txt'] },
              'GÚT DÂY': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/gút_dây/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/gút_dây', files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt'] },
              'PHƯƠNG HƯỚNG': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/phương_hướng/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/phương_hướng', files: ['bài_1.txt','bài_2.txt'] },
              'MẬT THƯ': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/mật_thư/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/mật_thư', files: ['bài_1.txt','bài_2.txt'] },
              'THƯỜNG THỨC': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/thường_thức/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/thường_thức', files: ['bài_1.txt'] },
              'TRUYỀN TIN': { introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/truyền_tin/giới_thiệu.txt', basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_thanh_niên/truyền_tin', files: ['bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt'] }
            }
          },
          'HOẠT ĐỘNG XÃ HỘI': {
            introFile: 'data/ngành_thiếu/sơ_thiện/hoạt_động_xã_hội/giới_thiệu.txt',
            basePath: 'data/ngành_thiếu/sơ_thiện/hoạt_động_xã_hội',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','bài_6.txt','bài_7.txt'
            ]
          },
          'VĂN NGHỆ': {
            introFile: 'data/ngành_thiếu/sơ_thiện/văn_nghệ/giới_thiệu.txt',
            basePath: 'data/ngành_thiếu/sơ_thiện/văn_nghệ',
            files: [
              'bài_1.txt','bài_2.txt','bài_3.txt','bài_4.txt','bài_5.txt','danh_sách_bài_hát.txt'
            ]
          }
        }
      }
    }
  }
};

function pushView(viewFn) {
  viewHistory.push(viewFn);
}

function goBack() {
  if (viewHistory.length <= 1) return;
  viewHistory.pop();
  const previous = viewHistory[viewHistory.length - 1];
  previous();
}

function clearButtons() {
  lessonButtons.innerHTML = '';
}

function setActiveButton(button) {
  if (activeButton) activeButton.classList.remove('active');
  activeButton = button;
  if (activeButton) activeButton.classList.add('active');
}

function createButton(label, onClick) {
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'lesson-button';
  btn.textContent = label;
  btn.addEventListener('click', () => onClick(btn));
  return btn;
}

function createBackButton() {
  if (viewHistory.length <= 1) return null;
  return createButton('« Quay lại', () => goBack());
}

function getFallbackTitle(filename) {
  const basename = filename.split('/').pop().split('\\').pop();
  return basename.replace('bài_', 'Bài ').replace('.txt', '');
}

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function isHeadingLine(line) {
  const trimmed = line.trim();
  if (!trimmed) return false;
  if (/^[IVXLCDM]+\./i.test(trimmed)) return true;
  if (/^[0-9]+[.)]\s+/.test(trimmed)) return true;
  if (/^[a-z][.)]\s+/.test(trimmed)) return true;
  return trimmed === trimmed.toUpperCase() && /[A-ZÀ-ỸỤƠƯÁÀẠẢẤẦẨẪẬẮẰẲẴẶÉÈẺẼẸÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴĐ]/.test(trimmed) && trimmed.length > 2;
}

function resolveImagePath(baseDir, src) {
  if (!src || /^(https?:|data:|\/)/i.test(src)) {
    return src;
  }
  if (!baseDir || baseDir === '.') {
    return src;
  }
  const result = `${baseDir}/${src}`;
  console.log(`[IMAGE DEBUG] baseDir="${baseDir}" src="${src}" result="${result}"`);
  return result;
}

function toImageSrc(path) {
  if (!path || /^(https?:|data:)/i.test(path)) {
    return path;
  }
  return encodeURI(path);
}

function formatLessonHTML(text, baseDir) {
  const lines = text.split(/\r?\n/);
  const htmlLines = [];
  let inList = false;
  const imageMarkdown = /^\s*!\[([^\]]*)\]\(([^)]+)\)\s*$/;
  const imageLine = /^\s*(?:!IMAGE|IMAGE|HÌNH ẢNH)[:\s]+(.+)$/i;
  const listItem = /^\s*[-*+]\s+(.+)$/;

  const closeList = () => {
    if (inList) {
      htmlLines.push('</ul>');
      inList = false;
    }
  };

  for (const line of lines) {
    if (line.trim() === '') {
      closeList();
      htmlLines.push('<div class="lesson-spacer"></div>');
      continue;
    }

    const markdownMatch = line.match(imageMarkdown);
    if (markdownMatch) {
      closeList();
      const alt = escapeHtml(markdownMatch[1].trim() || 'Hình ảnh');
      const rawSrc = markdownMatch[2].trim();
      console.log(`[FORMAT DEBUG] raw image src from markdown: "${rawSrc}"`);
      const src = toImageSrc(resolveImagePath(baseDir, rawSrc));
      console.log(`[FORMAT DEBUG] final src after resolve: "${src}"`);
      htmlLines.push(`<div class="lesson-image-wrapper"><img src="${escapeHtml(src)}" alt="${alt}" class="lesson-image" /><p class="lesson-image-caption">${alt}</p></div>`);
      continue;
    }

    const imageLineMatch = line.match(imageLine);
    if (imageLineMatch) {
      closeList();
      const src = toImageSrc(resolveImagePath(baseDir, imageLineMatch[1].trim()));
      htmlLines.push(`<div class="lesson-image-wrapper"><img src="${escapeHtml(src)}" alt="Hình ảnh" class="lesson-image" /></div>`);
      continue;
    }

    const listMatch = line.match(listItem);
    if (listMatch) {
      if (!inList) {
        htmlLines.push('<ul class="lesson-list-items">');
        inList = true;
      }
      htmlLines.push(`<li>${escapeHtml(listMatch[1].trim())}</li>`);
      continue;
    }

    closeList();
    const escaped = escapeHtml(line);
    if (isHeadingLine(line)) {
      htmlLines.push(`<p class="lesson-heading"><strong>${escaped}</strong></p>`);
      continue;
    }
    htmlLines.push(`<p>${escaped}</p>`);
  }

  closeList();
  return htmlLines.join('');
}

async function fetchTitleFromFile(path) {
  if (window.location.protocol === 'file:') return getFallbackTitle(path);
  try {
    const resp = await fetch(encodeURI(path));
    if (!resp.ok) return getFallbackTitle(path);
    const txt = await resp.text();
    const first = txt.split(/\r?\n/).find(l => l.trim().length > 0);
    return first ? first.trim() : getFallbackTitle(path);
  } catch {
    return getFallbackTitle(path);
  }
}

async function loadLesson(path, button) {
  setActiveButton(button);
  lessonTitleElement.classList.add('hidden');
  lessonOutput.classList.remove('hidden');
  lessonPlaceholder.classList.add('hidden');
  lessonOutput.textContent = 'Đang tải nội dung...';

  if (window.location.protocol === 'file:') {
    lessonTitleElement.textContent = getFallbackTitle(path);
    lessonTitleElement.classList.remove('hidden');
    lessonOutput.textContent = 'Trang đang được mở trực tiếp từ file. Vui lòng chạy server tĩnh (ví dụ: python -m http.server) và truy cập lại trang qua http://localhost.';
    return;
  }

  try {
    const resp = await fetch(encodeURI(path));
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const txt = await resp.text();
    console.log(`[LOAD DEBUG] path="${path}" first 500 chars: "${txt.substring(0, 500)}"`);
    const lines = txt.split(/\r?\n/);
    const idx = lines.findIndex(l => l.trim().length > 0);
    const title = idx >= 0 ? lines[idx].trim() : getFallbackTitle(path);
    const content = idx >= 0 ? lines.slice(idx + 1).join('\n').trim() : lines.join('\n').trim();
    const lessonDir = path.includes('/') ? path.slice(0, path.lastIndexOf('/')) : '.';
    lessonTitleElement.textContent = title;
    lessonTitleElement.classList.remove('hidden');
    lessonOutput.innerHTML = content ? formatLessonHTML(content, lessonDir) : '<p>[Không có nội dung khác ngoài tiêu đề]</p>';
  } catch (err) {
    lessonTitleElement.textContent = getFallbackTitle(path);
    lessonTitleElement.classList.remove('hidden');
    lessonOutput.textContent = `Lỗi khi tải nội dung: ${err.message}`;
  }
}

async function showLessonsList(basePath, files) {
  clearButtons();
  lessonTitleElement.classList.add('hidden');
  lessonOutput.classList.add('hidden');
  lessonPlaceholder.classList.remove('hidden');

  // Ensure bài_7 is included for gút_dây (some builds missed it)
  const fileList = Array.isArray(files) ? files.slice() : [];
  if (basePath && basePath.includes('gút_dây') && !fileList.includes('bài_7.txt')) {
    fileList.push('bài_7.txt');
  }

  for (const f of fileList) {
    const rel = basePath === '.' ? f : `${basePath}/${f}`;
    const title = await fetchTitleFromFile(rel);
    lessonButtons.appendChild(createButton(title, (btn) => loadLesson(rel, btn)));
  }

  const back = createBackButton();
  if (back) lessonButtons.appendChild(back);
}

async function showSectionIntro(introPath, basePath, files) {
  clearButtons();
  lessonTitleElement.classList.add('hidden');
  lessonOutput.classList.remove('hidden');
  lessonPlaceholder.classList.add('hidden');

  if (window.location.protocol === 'file:') {
    lessonOutput.textContent = 'Trang đang được mở trực tiếp từ file.';
    const back = createBackButton();
    if (back) lessonButtons.appendChild(back);
    return;
  }

  try {
    const resp = await fetch(encodeURI(introPath));
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const txt = await resp.text();
    const lines = txt.split(/\r?\n/);
    const idx = lines.findIndex(l => l.trim().length > 0);
    const title = idx >= 0 ? lines[idx].trim() : 'Giới thiệu';
    const content = idx >= 0 ? lines.slice(idx + 1).join('\n').trim() : lines.join('\n').trim();
    const introDir = introPath.includes('/') ? introPath.slice(0, introPath.lastIndexOf('/')) : '.';
    lessonTitleElement.textContent = title;
    lessonTitleElement.classList.remove('hidden');
    lessonOutput.innerHTML = content ? formatLessonHTML(content, introDir) : '<p>[Không có nội dung khác ngoài tiêu đề]</p>';
  } catch (err) {
    lessonOutput.textContent = `Lỗi khi tải giới thiệu: ${err.message}`;
  }

  // Add button to go to lessons list
  if (files && files.length > 0) {
    lessonButtons.appendChild(createButton('Danh sách bài học', () => {
      navigate(() => showLessonsList(basePath, files));
    }));
  }

  const back = createBackButton();
  if (back) lessonButtons.appendChild(back);
}

function showSections(sections) {
  clearButtons();
  lessonTitleElement.classList.add('hidden');
  lessonOutput.classList.add('hidden');
  lessonPlaceholder.classList.remove('hidden');

  for (const [label, info] of Object.entries(sections)) {
    lessonButtons.appendChild(createButton(label, async () => {
      if (info.introFile) {
        await navigate(() => showSectionIntro(info.introFile, info.basePath, info.files || []));
      } else if (info.sections) {
        await navigate(() => showSections(info.sections));
      } else if (info.files) {
        await navigate(() => showLessonsList(info.basePath, info.files));
      }
    }));
  }

  const back = createBackButton();
  if (back) lessonButtons.appendChild(back);
}

async function showCategories(sections) {
  clearButtons();
  lessonTitleElement.classList.add('hidden');
  lessonOutput.classList.add('hidden');
  lessonPlaceholder.classList.remove('hidden');

  for (const [label, info] of Object.entries(sections)) {
    lessonButtons.appendChild(createButton(label, async () => {
      if (info.introFile) {
        await navigate(() => showSectionIntro(info.introFile, info.basePath, info.files || []));
      } else if (info.sections) {
        await navigate(() => showSections(info.sections));
      } else if (info.files) {
        await navigate(() => showLessonsList(info.basePath, info.files));
      }
    }));
  }

  const back = createBackButton();
  if (back) lessonButtons.appendChild(back);
}

async function showRoot() {
  clearButtons();
  lessonTitleElement.classList.add('hidden');
  lessonOutput.classList.add('hidden');
  lessonPlaceholder.classList.remove('hidden');

  for (const [label, group] of Object.entries(structure)) {
    lessonButtons.appendChild(createButton(label, async () => {
      if (group.sections) {
        await navigate(() => showCategories(group.sections));
      } else if (group.files) {
        await navigate(() => showLessonsList(group.basePath, group.files));
      }
    }));
  }
}

async function navigate(viewFn) {
  viewHistory.push(viewFn);
  await viewFn();
}

function init() {
  viewHistory.length = 0;
  navigate(showRoot);
}

init();

