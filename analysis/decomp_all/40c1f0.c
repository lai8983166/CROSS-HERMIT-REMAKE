
void __thiscall FUN__text__0040c1f0(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int *local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((param_2 < 0) || (0x13 < param_2)) {
    iVar2 = FUN__text__00424f80("(0<=no) && (no<20)",
                                "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                DAT_005ff11c + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = (int *)(local_8 + 0x7194 + param_2 * 4);
  if (*local_c != 0) {
    iVar2 = FUN__text__00424f80("wk->ReadAddr==0",
                                "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                DAT_005ff11c + 5,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  *local_c = param_3;
  local_8 = 0x40c28e;
  FUN__text__0056ce80();
  return;
}

