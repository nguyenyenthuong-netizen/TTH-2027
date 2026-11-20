"""Exercise the embedded model through the public framework controls in the existing browser test."""
def check(page, width, form, out):
    page.locator('.tab[data-target="staffing"]').evaluate('(b)=>b.click()')
    host=page.locator('#dinh-bien-2027')
    host.locator('.app').wait_for(state='visible',timeout=10000)
    def pane(which):
        host.locator('[data-panel="'+which+'"]').click(timeout=12000)
        assert host.locator('#db-main h3').first.is_visible()
        dims=host.evaluate('h=>{const a=h.shadowRoot.querySelector(".app");return [a.clientWidth,a.scrollWidth,h.getBoundingClientRect().right]}')
        assert dims[1]<=dims[0]+2 and dims[2]<=width+18,(form,which,dims)
    pane('summary')
    base=host.locator('.metric b').nth(0).inner_text()
    host.locator('[data-set="scenario"]').select_option('high')
    assert host.locator('.metric b').nth(0).inner_text()!=base
    host.locator('[data-set="scenario"]').select_option('base')
    page.screenshot(path=str(out/('dinh-bien-'+form+'.jpg')),type='jpeg',quality=65,timeout=20000)
    pane('roles')
    rs=host.locator('[data-set="role"] option').evaluate_all('(a)=>a.map(x=>x.value)')
    assert len(rs)==26
    for rid in rs:
        host.locator('[data-set="role"]').select_option(rid)
        assert host.locator('#db-main h4').first.inner_text().strip()
        assert 'NaN' not in ''.join(host.locator('.metric').all_text_contents())
    pane('sites');host.locator('[data-set="site"]').select_option('vinh')
    old=host.locator('.metric b').nth(0).inner_text();vol=host.locator('[data-edit-site] [name=v2]');vol.fill(str(int(vol.input_value())+2));host.locator('[data-edit-site] button').click()
    assert host.locator('.metric b').nth(0).inner_text()!=old
    pane('manage');assert host.locator('#db-main').get_by_text('Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số',exact=True).count()>=1
    pane('docs');host.locator('[data-search="doc"]').fill('B-7');rec=host.locator('[data-doc-key="B-7~1"]');rec.locator('summary').first.click();rec.locator('[data-edit-doc]').wait_for();assert rec.locator('.inner').get_by_text('V3-B02',exact=False).count()>=1
    rec.locator('[name=count]').fill('2');rec.locator('[type=submit]').click();assert host.locator('[data-doc-key="B-7~1"] [name=count]').input_value()=='2'
    pane('flows');assert '568' in host.locator('[data-results="flow"] .count').inner_text();host.locator('[data-search="flow"]').fill('DA-hang-muc-01-01');flow=host.locator('[data-flow-index]').first;flow.locator('summary').first.click();flow.locator('.flowstep .entry summary').first.click();assert flow.get_by_text('Cách tính công',exact=True).is_visible()
    pane('audit');host.locator('[data-cap] [name=clinic]').fill('25');host.locator('[data-cap] button').click();assert host.locator('[data-cap] [name=clinic]').input_value()=='25'
    print('PASS Mục 05:',form,'7 nội dung, 26 chức danh, 3 kịch bản, sửa sản lượng và tài liệu, tra đầu ra, quỹ Clinic')
