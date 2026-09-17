
void tick_0x4551c0(undefined4 param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 auStack_58 [10];
  undefined *puStack_30;
  undefined4 uStack_18;
  int iStack_14;
  int iStack_10;
  int iStack_c;
  
  puVar3 = auStack_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  func_0x00497720();
  iStack_c = func_0x00455060(param_1,param_2);
  iStack_10 = func_0x00455060(param_1,param_2 + 1);
  (*API_KERNEL32_DLL_lstrcmpA)(iStack_c,&PTR_DAT_0059a60c);
  iVar2 = __chkesp();
  if ((iVar2 == 0) &&
     (iVar2 = FUN_00424f80(&DAT_0059a5dc,"E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                           DAT_0060cd9c + 0xc,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  iStack_14 = iStack_10 - iStack_c;
  func_0x00496d80(0);
  func_0x004ce460(iStack_c,0xffffffff,iStack_14);
  func_0x004ce030();
  (*API_KERNEL32_DLL_GetTickCount)();
  uStack_18 = __chkesp();
  do {
    iVar2 = func_0x004ce8f0();
  } while (iVar2 != 0);
  func_0x004d0790(1);
  func_0x004ce060();
  iVar2 = func_0x00496e30();
  if (iVar2 == 0) {
    func_0x00496d80(0);
  }
  else {
    func_0x00496d80(1);
  }
  puStack_30 = &UNK_004552fb;
  __chkesp();
  return;
}

