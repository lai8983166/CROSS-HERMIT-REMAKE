
void __fastcall FUN__text__004404a0(int param_1)

{
  code *pcVar1;
  undefined4 uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined4 local_60 [16];
  int local_20;
  int local_1c;
  int local_18;
  int local_14;
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar4 = local_60;
  for (iVar3 = 0x17; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  *(undefined4 *)(param_1 + 0x2646c) = 0x31c;
  *(undefined4 *)(param_1 + 0x26470) = 0x269;
  *(int *)(param_1 + 0x26474) = (int)*(short *)(param_1 + 0x264c4);
  *(int *)(param_1 + 0x26478) = (int)*(short *)(param_1 + 0x264c6);
  local_8 = param_1;
  FUN__text__004077c0(DAT_007a49fc);
  *(undefined2 *)(local_8 + 0x26544) = *(undefined2 *)(local_8 + 0x26474);
  *(undefined2 *)(local_8 + 0x26546) = *(undefined2 *)(local_8 + 0x26478);
  *(undefined4 *)(local_8 + 0x26540) = 0x19;
  uVar5 = 0;
  uVar2 = FUN__text__004142b0(0);
  local_c = FUN__text__00403bd0(uVar2,uVar5);
  if ((local_c != 0) &&
     (iVar3 = FUN__text__00424f80("ret==0","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ffa2c + 0x10,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  *(int *)(local_8 + 0x26590) =
       (int)*(short *)(local_8 + 0x26544) * (int)*(short *)(local_8 + 0x26546);
  local_10 = FUN__text__00428a40(*(int *)(local_8 + 0x26590) << 1);
  *(undefined4 *)(local_8 + 0x2658c) = local_10;
  if ((*(int *)(local_8 + 0x2658c) == 0) &&
     (iVar3 = FUN__text__00424f80("bgFogMem!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ffa2c + 0x14,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*(int *)(local_8 + 0x2658c) != 0) {
    _memset(*(void **)(local_8 + 0x2658c),0,4);
    local_14 = (int)**(short **)(local_8 + 0x2659c);
    *(float *)(local_8 + 0x2647c) = (float)local_14 / (float)*(int *)(local_8 + 0x26474);
    local_18 = (int)*(short *)(*(int *)(local_8 + 0x2659c) + 2);
    *(float *)(local_8 + 0x26480) = (float)local_18 / (float)*(int *)(local_8 + 0x26478);
    local_1c = (int)**(short **)(local_8 + 0x2659c);
    *(float *)(local_8 + 0x26484) = (float)*(int *)(local_8 + 0x26474) / (float)local_1c;
    local_20 = (int)*(short *)(*(int *)(local_8 + 0x2659c) + 2);
    *(float *)(local_8 + 0x26488) = (float)*(int *)(local_8 + 0x26478) / (float)local_20;
    FUN__text__00440a10();
    FUN__text__00440c10();
  }
  local_8 = 0x4406e1;
  FUN__text__0056ce80();
  return;
}

