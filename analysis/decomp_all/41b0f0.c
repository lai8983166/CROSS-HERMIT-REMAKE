
void FUN__text__0041b0f0(undefined4 param_1)

{
  code *pcVar1;
  undefined1 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_4c [16];
  undefined1 *local_c;
  int local_8;
  
  puVar4 = local_4c;
  for (iVar3 = 0x12; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_c = (undefined1 *)FUN__text__0041abf0(param_1);
  if (local_c == (undefined1 *)0x0) {
    iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                "E:\\CrossHermit\\GAME\\Src\\SYSTEM\\DIRECTX\\DxPlay.cpp",
                                DAT_005ff594 + 6,0);
    if (iVar3 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  else {
    *local_c = 0;
    _memset(local_c,0,0x88);
    uVar2 = FUN__text__0041acf0();
    *(undefined1 *)(local_8 + 0x2000) = uVar2;
  }
  local_8 = 0x41b188;
  FUN__text__0056ce80();
  return;
}

