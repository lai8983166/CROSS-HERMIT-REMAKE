
void FUN__text__00427060(undefined4 param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_2c58 [16];
  undefined4 local_2c18;
  undefined1 local_2c14 [1024];
  undefined1 *local_2814;
  undefined1 local_2810 [10184];
  undefined4 uStackY_48;
  undefined1 *puStackY_44;
  char *pcStackY_40;
  char *pcStackY_3c;
  char *pcStackY_38;
  undefined4 uStackY_34;
  uint uVar4;
  
  FUN__text__0056e230();
  puVar3 = local_2c58;
  for (iVar2 = 0xb15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_2814 = local_2810;
  uVar1 = FUN__text__0056cd38();
  FUN__text__0056cd68();
  uStackY_34 = 0x4270bf;
  _memset(local_2810,0,0x2800);
  pcStackY_38 = "h\x1cMY";
  uStackY_34 = uVar1;
  FUN__text__0056cd68();
  pcStackY_38 = "ab";
  pcStackY_3c = "test1.txt";
  pcStackY_40 = (char *)0x4270e7;
  local_2c18 = FUN__text__0056e7c0();
  pcStackY_38 = "=======================\r\n";
  pcStackY_40 = (char *)0x427101;
  pcStackY_3c = (char *)local_2c18;
  FUN__text__0056e5f0();
  DAT_0079fc70 = *(undefined4 *)(local_2814 + 8);
  for (uVar4 = 0; uVar4 < *(uint *)(local_2814 + 8); uVar4 = uVar4 + 1) {
    pcStackY_38 = local_2814 + *(int *)(local_2814 + uVar4 * 4 + 0x18);
    pcStackY_3c = (char *)(uVar4 + 1);
    pcStackY_40 = "%2d. %s\r\n";
    puStackY_44 = local_2c14;
    uStackY_48 = 0x427161;
    (*API_USER32_DLL_wsprintfA)();
    pcStackY_38 = (char *)0x42716b;
    FUN__text__0056ce80();
    pcStackY_38 = local_2c14;
    pcStackY_3c = &DAT_0079aa44 + uVar4 * 200;
    pcStackY_40 = (char *)0x427187;
    FUN__text__0056cd90();
    pcStackY_38 = local_2c14;
    pcStackY_3c = (char *)local_2c18;
    pcStackY_40 = (char *)0x42719d;
    FUN__text__0056e5f0();
  }
  pcStackY_38 = (char *)local_2c18;
  pcStackY_3c = (char *)0x4271b1;
  FUN__text__0056e4a0();
  pcStackY_3c = (char *)param_1;
  pcStackY_40 = (char *)0x4271c1;
  pcStackY_38 = (char *)uVar1;
  FUN__text__0056cd2c();
  FUN__text__0056ce80();
  return;
}

