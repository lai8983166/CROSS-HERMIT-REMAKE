
void FUN__text__004d6cb0(undefined4 param_1)

{
  char cVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 local_938 [16];
  undefined4 local_8f8 [131];
  int local_6ec;
  undefined1 local_6e8 [259];
  char local_5e5 [513];
  undefined4 local_3e4;
  char local_3e0 [74];
  char local_396;
  char local_395;
  char local_391;
  char local_390;
  char local_38c;
  char local_383;
  char local_382;
  char local_381;
  char local_380;
  char local_37e;
  char local_37d;
  char local_37b;
  char local_37a;
  char local_378;
  char local_377;
  char local_375;
  char local_374;
  undefined4 local_2e0;
  short local_270;
  short local_26c;
  undefined2 local_268;
  undefined4 local_264;
  undefined1 local_260 [2];
  short local_25e;
  short local_25c;
  short local_25a;
  short local_258;
  short local_256;
  short local_254;
  short local_252;
  short local_250;
  short local_24e;
  uint local_24c [11];
  char local_220 [276];
  undefined1 local_10c [248];
  undefined4 uStack_14;
  int local_8;
  
  puVar3 = local_938;
  for (iVar2 = 0x24d; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  FUN__text__0056cd90(local_10c,param_1);
  _memset(local_24c,0,0x140);
  (*DAT_005921f4)(local_10c,local_24c);
  local_264 = FUN__text__0056ce80();
  local_268 = 0;
  puVar3 = &DAT_005c8220;
  puVar4 = &local_2e0;
  for (iVar2 = 0x1b; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = *puVar3;
    puVar3 = puVar3 + 1;
    puVar4 = puVar4 + 1;
  }
  *(undefined2 *)puVar4 = *(undefined2 *)puVar3;
  *(undefined1 *)((int)puVar4 + 2) = *(undefined1 *)((int)puVar3 + 2);
  *(undefined2 *)(local_8 + 0x19aac) = 0;
  do {
    if (((local_24c[0] & 0x10) != 0) && (iVar2 = _strcmp(local_220,".."), iVar2 != 0)) {
      _strcmp(local_220,".");
    }
    if ((((local_24c[0] & 0x10) != 0x10) && (*(short *)(local_8 + 0x19aac) != 200)) &&
       (iVar2 = FUN__text__00429aa0(local_220), iVar2 != 0)) {
      local_3e4 = FUN__text__00450230(local_220);
      FUN__text__004296b0(local_3e4,local_6e8);
      cVar1 = FUN__text__004d73c0(local_3e4,local_260);
      if (cVar1 != '\0') {
        FUN__text__0056cd90(local_3e0,&local_2e0);
        for (local_26c = 0; (local_26c < 0x40 && (local_5e5[local_26c] != '\0'));
            local_26c = local_26c + 1) {
          local_3e0[local_26c] = local_5e5[local_26c];
        }
        local_396 = ' ';
        if ((int)local_25e / 10 != 0) {
          local_396 = (char)((int)local_25e / 10) + '0';
        }
        local_395 = (char)((int)local_25e % 10) + '0';
        local_391 = (char)((int)local_25c / 10) + '0';
        local_390 = (char)((int)local_25c % 10) + '0';
        local_38c = (char)((int)local_25a % 10) + '0';
        local_383 = (char)(((int)local_258 / 1000) % 10) + '0';
        local_382 = (char)(((int)local_258 / 100) % 10) + '0';
        local_381 = (char)(((int)local_258 / 10) % 10) + '0';
        local_380 = (char)((int)local_258 % 10) + '0';
        local_37e = (char)(((int)local_256 / 10) % 10) + '0';
        local_37d = (char)((int)local_256 % 10) + '0';
        local_37b = (char)(((int)local_254 / 10) % 10) + '0';
        local_37a = (char)((int)local_254 % 10) + '0';
        local_378 = (char)(((int)local_252 / 10) % 10) + '0';
        local_377 = (char)((int)local_252 % 10) + '0';
        local_375 = (char)(((int)local_250 / 10) % 10) + '0';
        local_374 = (char)((int)local_250 % 10) + '0';
        local_6ec = ((int)local_258 % 100) * 0x1ea6e00 + local_256 * 0x28de80 + local_254 * 0x15180
                    + local_252 * 0xe10 + local_250 * 0x3c + (int)local_24e;
        FUN__text__0056cd90(local_8 + 0x14c + *(short *)(local_8 + 0x19aac) * 0x20c,local_5e5);
        FUN__text__0056cd90(local_8 + 0x250 + *(short *)(local_8 + 0x19aac) * 0x20c,local_3e0);
        *(int *)(local_8 + 0x354 + *(short *)(local_8 + 0x19aac) * 0x20c) = local_6ec;
        *(short *)(local_8 + 0x19aac) = *(short *)(local_8 + 0x19aac) + 1;
      }
    }
    (*API_KERNEL32_DLL_FindNextFileA)(local_264,local_24c);
    iVar2 = FUN__text__0056ce80();
  } while (iVar2 != 0);
  for (local_26c = 0; (int)local_26c < *(short *)(local_8 + 0x19aac) + -1; local_26c = local_26c + 1
      ) {
    for (local_270 = local_26c; local_270 < *(short *)(local_8 + 0x19aac); local_270 = local_270 + 1
        ) {
      if (*(uint *)(local_8 + 0x354 + local_26c * 0x20c) <
          *(uint *)(local_8 + 0x354 + local_270 * 0x20c)) {
        puVar3 = (undefined4 *)(local_8 + 0x14c + local_26c * 0x20c);
        puVar4 = local_8f8;
        for (iVar2 = 0x83; iVar2 != 0; iVar2 = iVar2 + -1) {
          *puVar4 = *puVar3;
          puVar3 = puVar3 + 1;
          puVar4 = puVar4 + 1;
        }
        puVar3 = (undefined4 *)(local_8 + 0x14c + local_270 * 0x20c);
        puVar4 = (undefined4 *)(local_8 + 0x14c + local_26c * 0x20c);
        for (iVar2 = 0x83; iVar2 != 0; iVar2 = iVar2 + -1) {
          *puVar4 = *puVar3;
          puVar3 = puVar3 + 1;
          puVar4 = puVar4 + 1;
        }
        puVar3 = local_8f8;
        puVar4 = (undefined4 *)(local_8 + 0x14c + local_270 * 0x20c);
        for (iVar2 = 0x83; iVar2 != 0; iVar2 = iVar2 + -1) {
          *puVar4 = *puVar3;
          puVar3 = puVar3 + 1;
          puVar4 = puVar4 + 1;
        }
      }
    }
  }
  for (local_26c = 0; local_26c < *(short *)(local_8 + 0x19aac); local_26c = local_26c + 1) {
    FUN__text__004d6150(local_8 + 0x250 + local_26c * 0x20c);
  }
  (*API_KERNEL32_DLL_FindClose)(local_264);
  FUN__text__0056ce80();
  uStack_14 = 0x4d73b5;
  FUN__text__0056ce80();
  return;
}

