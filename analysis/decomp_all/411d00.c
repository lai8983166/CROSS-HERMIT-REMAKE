
void __fastcall FUN__text__00411d00(int param_1)

{
  char cVar1;
  short sVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_54 [16];
  int local_14;
  char local_10;
  undefined3 uStack_f;
  uint local_c;
  int local_8;
  
  puVar4 = local_54;
  for (iVar3 = 0x14; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  _memset((void *)(param_1 + 0xc),0,0x100);
  for (local_14 = 0; local_14 != 0x90; local_14 = local_14 + 1) {
    local_c = CONCAT31(local_c._1_3_,(&DAT_005ff36c)[local_14 * 2]);
    cVar1 = (&DAT_005ff36d)[local_14 * 2];
    _local_10 = CONCAT31(uStack_f,cVar1);
    if (cVar1 != -1) {
      (*API_USER32_DLL_GetAsyncKeyState)(cVar1);
      sVar2 = FUN__text__0056ce80();
      if (((int)sVar2 & 0x8000U) != 0) {
        *(undefined1 *)(local_8 + 0xc + (local_c & 0xff)) = 0x80;
      }
    }
  }
  (*API_USER32_DLL_GetAsyncKeyState)(0x11);
  sVar2 = FUN__text__0056ce80();
  if (((int)sVar2 & 0x8000U) != 0) {
    *(undefined1 *)(local_8 + 0x29) = 0x80;
    *(undefined1 *)(local_8 + 0x77) = 0x80;
  }
  local_c = 0x411dea;
  FUN__text__0056ce80();
  return;
}

