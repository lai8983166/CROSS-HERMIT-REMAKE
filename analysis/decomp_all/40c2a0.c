
void __thiscall FUN_0040c2a0(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int *local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((param_2 < 0) || (0x13 < param_2)) {
    iVar2 = FUN_00424f80("(0<=no) && (no<20)",
                         "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",DAT_005ff120 + 3
                         ,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = (int *)(local_8 + 0x7194 + param_2 * 4);
  if (*local_c != 0) {
    local_10 = *local_c;
    FUN_00428ad0(local_10);
    *local_c = 0;
  }
  local_8 = 0x40c32f;
  __chkesp();
  return;
}

