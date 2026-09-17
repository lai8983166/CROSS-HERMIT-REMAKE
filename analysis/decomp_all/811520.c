
bool FUN__text1__00811520(byte *param_1,int *param_2,int param_3)

{
  void *pvVar1;
  int iVar2;
  int iVar3;
  uint *puVar4;
  byte *local_c;
  uint local_8;
  
  FUN__text1__00811873();
  FUN__text1__008118e1();
  pvVar1 = operator_new(param_3 + 1);
  FUN__text1__00811723(pvVar1,param_3,1);
  iVar3 = *param_2;
  local_8 = (uint)*param_1;
  local_c = param_1;
  while ((local_c = local_c + 1, local_c < param_1 + iVar3 && (DAT_00874430 == '\0'))) {
    iVar2 = FUN__text1__00811942(local_8,*local_c);
    puVar4 = (uint *)(DAT_00874448 + iVar2 * 0xc);
    if (*puVar4 == 0xffffffff) {
      *puVar4 = DAT_00874424;
      DAT_00874424 = DAT_00874424 + 1;
      puVar4[1] = local_8;
      *(byte *)(puVar4 + 2) = *local_c;
      FUN__text1__008117b5(local_8,DAT_00874444);
      iVar2 = DAT_00874444;
      local_8 = (uint)*local_c;
      if (DAT_00874424 < 0x8000) {
        if (DAT_00874434 < DAT_00874424) {
          DAT_00874444 = DAT_00874444 + 1;
          FUN__text1__008117b5(0x101,iVar2);
          DAT_00874434 = DAT_00874434 << 1 | 1;
        }
      }
      else {
        FUN__text1__008117b5(0x102,DAT_00874444);
        FUN__text1__008118e1();
      }
    }
    else {
      local_8 = *puVar4;
    }
  }
  if (DAT_00874430 == '\0') {
    FUN__text1__008117b5(local_8,DAT_00874444);
    FUN__text1__008117b5(0x100,DAT_00874444);
  }
  if (DAT_00874430 == '\0') {
    iVar3 = FUN__text1__00811789();
    *param_2 = iVar3;
    FUN__text1__00848490(param_1,pvVar1,*param_2);
  }
  FUN__text1__00848476(pvVar1);
  FUN__text1__008118ae();
  return DAT_00874430 == '\0';
}

