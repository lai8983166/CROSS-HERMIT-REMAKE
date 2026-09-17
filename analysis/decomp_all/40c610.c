
void __thiscall FUN__text__0040c610(int param_1,int param_2,int param_3)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  undefined4 local_18;
  int local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_3;
  if (((*(int *)(param_1 + 8) != 0) && (*(int *)(param_1 + 0xc) != 0)) &&
     (*(int *)(param_1 + 0x10) != 0)) {
    local_8 = param_1;
    FUN__text__0040d120(param_2);
    FUN__text__0040c1f0(param_2,param_3);
    if (((param_2 < 0) || (0x13 < param_2)) &&
       (iVar2 = FUN__text__00424f80("(0<=no)&&(no<20)",
                                    "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                    DAT_005ff128 + 0xd,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if (((*(int *)(local_c + 4) < 0) || (0x77 < *(int *)(local_c + 4))) &&
       (iVar2 = FUN__text__00424f80("(0<=file->rcnt)&&(file->rcnt<120)",
                                    "E:\\CrossHermit\\GAME\\src\\SYSTEM\\DIRECTX\\DXAudio.CPP",
                                    DAT_005ff128 + 0xe,0), iVar2 != 0)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    for (local_10 = 0; local_10 != *(int *)(local_c + 4); local_10 = local_10 + 1) {
      local_18 = FUN__text__004214f0(local_c,local_10);
      local_14 = FUN__text__0040cc80(local_8 + 0x14 + param_2 * 0x5a0 + local_10 * 0xc,local_18);
      if (local_14 != 0) {
        FUN__text__0040d120(param_2);
        break;
      }
    }
  }
  local_8 = 0x40c770;
  FUN__text__0056ce80();
  return;
}

