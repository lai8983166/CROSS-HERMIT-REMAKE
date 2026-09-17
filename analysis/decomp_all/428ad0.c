
void FUN_00428ad0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (param_1 != 0) {
    local_8 = FUN_0056f830(param_1,1);
    if ((local_8 == 0) &&
       (iVar2 = FUN_00424f80("size!=0","E:\\CrossHermit\\GAME\\src\\system\\SysMem.cpp",
                             DAT_005ff6dc + 7,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    DAT_0079fc74 = DAT_0079fc74 - local_8;
    __free_dbg(param_1,1);
  }
  local_8 = 0x428b55;
  __chkesp();
  return;
}

